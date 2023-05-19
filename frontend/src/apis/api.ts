import { API } from "aws-amplify";

export class ApiRequest {
  static async get<T>(
    path: string,
    params?: {
      [key: string]: any;
    },
    headers?: {
      [key: string]: any;
    }
  ): Promise<T | null> {
    const apiName = "sbc-api";
    // const path = "/users";
    const myInit = {
      headers: headers, // OPTIONAL
      response: false, // OPTIONAL (return the entire Axios response object instead of only response.data)
      queryStringParameters: {},
      //    {
      //   name: "param", // OPTIONAL
      // },
    };

    if (params) {
      myInit.queryStringParameters = params;
    }

    return API.get(apiName, `/${path}`, myInit)
      .then((response) => {
        return response.data as T;
        // Add your code here
      })
      .catch((error) => {
        console.log(error.response);

        return null;
      });
  }
}
