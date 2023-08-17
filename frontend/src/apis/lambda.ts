import axios from "axios";
import { useProjectStore } from "../stores/projects";
import { useUserStore } from "../stores/user";
const LOG = true;

const SBC_DS_URL = `${import.meta.env.VITE_SBC_API_URL}/data-service`;
export const SBC_TW_URL = `${import.meta.env.VITE_SBC_API_URL}/twilio`;
const SBC_GET_BUCKET =
  "https://w75w7350kh.execute-api.us-west-2.amazonaws.com/production/sbcGetBucket";
const SBC_AI_URL =
  "https://w75w7350kh.execute-api.us-west-2.amazonaws.com/production/sbcOpenAI";

export async function downloadObjects(
  objects: any,
  context: any,
  tablePrefix = "",
  LOG = false
) {
  for (let objName in objects) {
    if (LOG) {
      console.log(
        "preparing to download object:" +
          objName +
          " prj_id=" +
          useProjectStore().prj_id
      );
    }
    // objName must match a sql table name (with prefix, if needed)
    const attributes = Object.keys(objects[objName]);
    const tableName = tablePrefix + objName;
    const filterClause = tableName.startsWith("lu_")
      ? ""
      : "prj_id=" + useProjectStore().prj_id;
    context[objName] = await downloadObject(
      tableName,
      attributes,
      filterClause,
      LOG
    );
  }
}

async function downloadSetup(
  tableName: any,
  attributes: any,
  filterClause: string = ""
) {
  const objectClause = "?object=" + tableName;
  // objName must match an object array; only the first element is used to get its attributes
  const attributesClause = "&attributes=" + attributes.join(",");
  // object / table names starting  with 'lu_' are lookup tables; all others require a prj_id
  const request =
    objectClause +
    attributesClause +
    (filterClause == "" ? "" : "&" + filterClause);
  const response = await axios.get(SBC_DS_URL + request, {
    headers: { Authorization: `Bearer ${useUserStore().token}` },
  });
  return response.data;
}

export async function downloadObject(
  tableName: any,
  attributes: any,
  filterClause: string = "",
  LOG: boolean = false
) {
  const response = await downloadSetup(tableName, attributes, filterClause);
  const responseList = [];
  for (let i = 0; i < response.length; i++) {
    const tempObj: any = {};
    for (let j = 0; j < attributes.length; j++) {
      tempObj[attributes[j]] = response[i][j];
    }
    responseList[i] = tempObj;
  }
  return responseList;
}

export async function downloadDictionary(
  tableName: any,
  attributes: any,
  filterClause: string = "",
  keyIndex: number
) {
  const response = await downloadSetup(tableName, attributes, filterClause);
  const responseDictionary: any = {};
  for (let i = 0; i < response.length; i++) {
    const tempObj: any = {};
    for (let j = 0; j < attributes.length; j++) {
      tempObj[attributes[j]] = response[i][j];
    }
    responseDictionary[response[i][keyIndex]] = tempObj;
  }
  return responseDictionary;
}

export async function getId(
  tableName: any,
  filterClause: any,
  LOG: boolean = false
) {
  const objectClause = "?object=" + tableName;
  const attributesClause = "&attributes=id&";
  const request = objectClause + attributesClause + filterClause;
  if (LOG) console.log(request);
  const response = await axios.get(SBC_DS_URL + request);
  let id = null;
  if (response.data.length > 0) {
    id = response.data[0][0];
  }
  if (LOG) console.log("id=" + id);
  return id;
}

export async function insert(tableName: any, attributes: any, LOG = false) {
  const payload: any = {};
  payload["object"] = tableName;
  if (!["users", "projects", "project_users"].includes(tableName)) {
    attributes["prj_id"] = useProjectStore().prj_id;
  }
  attributes["editing_user_id"] = useUserStore().id;
  payload["attributes"] = attributes;
  if (LOG) console.log(payload);
  const response = await axios.post(SBC_DS_URL, payload, {
    headers: { Authorization: `Bearer ${useUserStore().token}` },
  });
  const new_id = response.data[0][0];
  if (LOG) console.log(new_id);
  return new_id;
}

export async function update(
  tableName: any,
  id: any,
  attributes: any,
  LOG = false
) {
  const payload: any = {};
  payload["object"] = tableName;
  payload["id"] = id;
  attributes["editing_user_id"] = useUserStore().id;
  payload["attributes"] = attributes;
  if (LOG) console.log(payload);
  const response = await axios.put(SBC_DS_URL, payload, {
    headers: { Authorization: `Bearer ${useUserStore().token}` },
  });
}

export async function remove(tableName: any, ids: any, LOG = false) {
  const payload: any = {};
  payload["object"] = tableName;
  payload["ids"] = ids;
  if (LOG) console.log(payload);
  const response = await axios.delete(SBC_DS_URL, {
    data: payload,
    headers: { Authorization: `Bearer ${useUserStore().token}` },
  });
}

function countWords(str: string) {
  // Use a regular expression to match words, including words with apostrophes and hyphens
  const words = str.match(/\b[\w'-]+\b/g);

  // Return the number of words
  return words ? words.length : 0;
}

export async function getBucket(request_id: string) {
  const queryString = "?request_id=" + request_id;
  const maxAttempts = 30;
  let attempts = 0;

  const fetchBucket = async (): Promise<any> => {
    console.log("attempts=" + attempts);
    try {
      const response = await axios.get(SBC_GET_BUCKET + queryString);

      if (response.status === 200) {
        return response.data;
      } else if (response.status === 404 && attempts < maxAttempts) {
        attempts++;
        await new Promise((resolve) => setTimeout(resolve, 5000));
        return fetchBucket();
      } else {
        throw new Error(`Request failed with status code: ${response.status}`);
      }
    } catch (error) {
      if (
        error.response &&
        error.response.status === 404 &&
        attempts < maxAttempts
      ) {
        attempts++;
        await new Promise((resolve) => setTimeout(resolve, 5000));
        return fetchBucket();
      } else {
        throw error;
      }
    }
  };

  return fetchBucket();
}

export async function gptCompletion(
  prompt: string,
  context: string = null,
  format: string = null,
  start: string = null,
  stop: string = null
) {
  // format can be "item","list","sentence", or "paragraph"
  const { prj_id } = useProjectStore();
  const payload = { prj_id, prompt, format, stop, start, context };

  if (format) payload.format = format;
  if (start) payload.start = start;
  if (stop) payload.stop = stop;
  if (context) {
    console.log(
      "Words in GPT context + prompt: ",
      countWords(prompt) + countWords(context)
    );
    payload.context = context;
  }

  // set to false when testing other features to avoid unnecessary calls to openai
  if (true) {
    try {
      return axios
        .post(`${import.meta.env.VITE_SBC_API_URL}/open-ai`, payload, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${useUserStore().token}`,
          },
        })
        .then((resp) => resp.data.result);
    } catch (error) {
      console.error("Error:", error);
    }
  } else {
    return null;
  }
}

export async function twilioBroadcast(message: string, topic: string) {
  const payload: any = {};
  payload["message"] = message;
  payload["prj_id"] = useProjectStore().prj_id;
  payload["user_id"] = useUserStore().id;
  payload["user_name"] = useUserStore().address_as;
  payload["prj_name"] = useProjectStore().projectName;
  payload["related_item"] = topic;
  if (LOG) {
    console.log("characters in message:", message.length);
    console.log(payload);
  }
  const response = await axios.post(`${SBC_TW_URL}`, payload);
  if (LOG) console.log(response);
}
