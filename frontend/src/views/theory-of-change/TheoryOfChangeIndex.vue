<script  setup>
import mermaidAPI from "/node_modules/mermaid/dist/mermaid.esm.mjs";
import { onMounted, onUnmounted, reactive, ref, computed } from "vue";
import { useSideNavStore } from "@/stores/sideNav";
import axios from "axios";
import { onClickOutside } from "@vueuse/core";
import IndicatorBrowserPanel from "./IndicatorBrowserPanel.vue";
import { ApiRequest } from "@/apis/api";
import TheoryOfChangeItemModalVue from "./TheoryOfChangeItemModal.vue";

const isPanelVisible = ref(false);
const showIndicatorModal = ref(false);
const modalConfig = ref({
  isVisible: false,
  itemId: null,
  isItemNew: false,
  theoryOfChangeId: null
});

const svgUrl = ref("");
const svgImgSrcUrl = ref("");
const diagramContainer = ref(null);
const addNodeLabel = ref("");
const addNodeLogicModel = ref("");
const fromNodeId = ref(null);
const selectedNodeId = ref(null);
const selectedEdge = ref(null);
const selectedNode = ref(null);
const deleteFromId = ref(null);
const deleteToId = ref(null);
const textToImport = ref(null);
const logicModelView = ref(false);
let tempNavHidden = false;
const selectedExampleToC = ref(null);

const incomingEdges = computed(() =>
  diagram.edges.filter((e) => e.toId === selectedNodeId.value)
);
const outgoingEdges = computed(() =>
  diagram.edges.filter((e) => e.fromId === selectedNodeId.value)
);

const mermaidConfig = {
  startOnLoad: true,
  securityLevel: "loose",
  flowchart: {
    htmlLabels: false,
    curve: "basis",
  },
  theme: "default",
  themeVariables: {
    primaryColor: "#304148",
    edgeLabelBackground: "rgba(255, 255, 255, 0.7)",
    lineWidth: 1.5,
  },
  flowchart: {
    diagramPadding: 8,
    htmlLabels: true,
    nodeSpacing: 50,
    rankSpacing: 50,
    curve: "linear",
  },
};


const drawDiagram = async function () {
  const { svg } = await mermaidAPI.render("graphDiv", diagram.toMermaid());
  if (diagramContainer.value) {
    diagramContainer.value.innerHTML = "";
    const svgWrapper = document.createElement("div");
    svgWrapper.innerHTML = svg;
    const svgElement = svgWrapper.firstChild;
    diagramContainer.value.appendChild(svgElement);

    // Add click event listeners to the nodes manually
    const nodes = diagramContainer.value.querySelectorAll(".node");
    nodes.forEach((node) => {
      let clickTimeout;
      let isSingleClick = true;

      node.addEventListener("click", (event) => {
        let target = event.target;
        while (target && !target.classList.contains("node")) {
          target = target.parentElement;
        }
        const nodeId = target.id;
        const actualNodeId = nodeId.split("-")[1];

        if (isSingleClick) {
          clickTimeout = setTimeout(() => {
            if (isSingleClick) {
              window.nodeClick(actualNodeId);
            }
          }, 250);
        }
      });

      node.addEventListener("dblclick", (event) => {
        console.log("NODE");

        isSingleClick = false;
        clearTimeout(clickTimeout);

        let target = event.target;
        while (target && !target.classList.contains("node")) {
          target = target.parentElement;
        }
        const nodeId = target.id;
        const actualNodeId = nodeId.split("-")[1];

        window.nodeDoubleClick(actualNodeId);

        setTimeout(() => {
          isSingleClick = true;
        }, 250);
      });
    });

    // Add double-click event listeners to the edge labels
    const edgeLabels = diagramContainer.value.querySelectorAll("g.edgeLabel");
    const edgePaths = diagramContainer.value.querySelectorAll("g.edgePaths > path");
    edgeLabels.forEach((edgeLabel, index) => {
      edgeLabel.addEventListener("dblclick", (event) => {
        const edgePath = edgePaths[index];

        // Extract the source and target node IDs from the edge path's id attribute
        const edgePathId = edgePath.getAttribute("id");
        const [sourceNodeId, targetNodeId] = edgePathId.split("-").slice(1, 3);

        window.edgeDoubleClick(sourceNodeId, targetNodeId);
      });
    });
  }
};

function nodesToSubgraph(nodes, category) {
  let result = "";
  // console.log('nodesToSubgraph('+category+')');
  // console.log(nodes);
  const arrayInCategory = Object.fromEntries(
    Object.entries(nodes).filter(([, node]) => node.logicModel === category)
  );
  // console.log('type:'+typeof(arrayInCategory));
  // console.log('arrayInCategory',arrayInCategory);
  // console.log('arrayInCategory.length',arrayInCategory.length);
  if (Object.keys(arrayInCategory).length) {
    result += "subgraph " + (category == "" ? "no category" : category) + "\n";
    for (const key in arrayInCategory) {
      result += `${nodes[key].id}[${nodes[key].label}]\n`;
    }
    result += "end\n";
  }
  // console.log('result:'+result);
  return result;
}

function Node(id, label, defaultProperties) {
  const mergedProperties = Object.assign({}, defaultProperties, { id, label });
  this.id = mergedProperties.id;
  this.label = mergedProperties.label;
  this.description = mergedProperties.description;
  this.validated = mergedProperties.validated;
  this.indicator = mergedProperties.indicator;
  this.sem = mergedProperties.sem;
  this.logicModel = mergedProperties.logicModel;
  this.audience = mergedProperties.audience;
}

function Edge(fromNodeId, toNodeId) {
  this.fromId = fromNodeId;
  this.toId = toNodeId;
}

const diagram = reactive({
  defaultNode: {
    id: "",
    label: "",
    description: "",
    validated: false,
    indicator: "",
    sem: "",
    logicModel: "",
    audience: [],
  },
  defaultEdge: {
    fromId: 0,
    toId: 0,
    assumptions: "",
    risks: ""
  },
  diagramType: "flowchart",
  orientationIndex: 0,
  orientationOptions: ["LR", "TB", "RL", "BT"],
  nextNodeId: "Aa",
  nodes: {},
  edges: [],
  edgeSet: new Set(),

  edgeLabel(edge, fromOrTo) {
    if (fromOrTo == 'from') {
      return this.nodes[edge.fromId].label;
    }
    return this.nodes[edge.toId].label
  },
  orientation: function () {
    return this.orientationOptions[this.orientationIndex];
  },
  rotate: function () {
    this.orientationIndex++;
    if (this.orientationIndex == 4) this.orientationIndex = 0;
  },
  parseJSON: function (jsonString) {
    const inputObjects = JSON.parse(jsonString);
    for (const node of inputObjects.nodes) {
      // Merge the input object with the default node, so any missing properties are filled in
      const mergedNode = Object.assign({}, this.defaultNode, node);
      this.nodes[mergedNode.id] = mergedNode;
    }
    for (const edge of inputObjects.edges) {
      this.createEdge(edge.fromId, edge.toId, false);
    }
    drawDiagram();
  },
  parseGraph: function (graph) {
    console.log('parseGraph');
    console.log(graph);

    // const inputObjects = JSON.parse(jsonString);
    // for (const node of inputObjects.nodes) {
    //   // Merge the input object with the default node, so any missing properties are filled in
    //   const mergedNode = Object.assign({}, this.defaultNode, node);
    //   this.nodes[mergedNode.id] = mergedNode;
    // }
    // for (const edge of inputObjects.edges) {
    //   this.createEdge(edge.fromId, edge.toId, false);
    // }
    // drawDiagram();
  },

  createNode: function (label, logicModel) {
    const node = new Node(this.nextNodeId, label, this.defaultNode);
    node.logicModel = logicModel;
    this.nodes[this.nextNodeId] = node;
    this.nextNodeId =
      String.fromCharCode(this.nextNodeId.charCodeAt(0) + 1) + this.nextNodeId.charAt(1);

    drawDiagram();

    // TODO: replace id with current project id
    const id = 1
    ApiRequest.post(`theory-of-change/${id}/item`, {
      name: label,
      type_id: 1,
      from_id: null,
      to_id: null,
      sem_id: 1,
      description: "dummy description"
    })
      .then(resp => console.log(resp))

    return node;
  },

  createEdge: function (fromNodeId, toNodeId, draw = true) {
    console.log('createEdge:' + fromNodeId + toNodeId + draw);
    if (fromNodeId == toNodeId) return; // prevent double click from creating a useless self-edge
    const key = `${fromNodeId}|${toNodeId}`;
    if (!this.edgeSet.has(key)) {
      const newEdge = new Edge(fromNodeId, toNodeId);
      // Merge the input object with the default node, so any missing properties are filled in
      const mergedEdge = Object.assign({}, this.defaultEdge, newEdge);
      this.edges.push(mergedEdge);
      this.edgeSet.add(key);
      if (draw) {
        drawDiagram();
      }
      return mergedEdge;
    }
  },
  toMermaid: function () {
    let result = this.diagramType + " " + this.orientation() + "\n";
    if (logicModelView.value) {
      result += nodesToSubgraph(this.nodes, "impact");
      result += nodesToSubgraph(this.nodes, "outcome");
      result += nodesToSubgraph(this.nodes, "intermediate_outcome");
      result += nodesToSubgraph(this.nodes, "output");
      result += nodesToSubgraph(this.nodes, "activity");
      result += nodesToSubgraph(this.nodes, "");
    } else {
      for (const key in this.nodes) {
        result += `${this.nodes[key].id}[${this.nodes[key].label}]\n`;
      }
    }
    for (const edge of this.edges) {
      result += `${edge.fromId} -->|factors| ${edge.toId}\n`;
    }
    console.log(result);
    return result;
  },
  toJSON: function (inputNodes, edges) {
    const nodes = Object.values(inputNodes);
    return JSON.stringify({ nodes, edges });
  },
});

const fetchGraph = async (project_id) => {
  try {
    const id = 1
    const resp = await ApiRequest.get(`theory-of-change/${id}`);

    console.log(resp)
    // if (!response.ok) {
    //   throw new Error(`HTTP error! status: ${response.status}`);
    // }
    // const jsonText = await response.text();
    // console.log("here we go");
    // console.log(jsonText);
    // diagram.parseJSON(jsonText);
  } catch (error) {
    console.error('Failed to fetch JSON data:', error);
  }
}

onMounted(() => {
  fetchGraph(1)

  mermaidAPI.initialize(mermaidConfig);

  window.addEventListener("keydown", escapeKeyHandler);

  window.edgeDoubleClick = function (fromNodeId, toNodeId) {
    console.log(fromNodeId, toNodeId); //selectedEdgeIds
    const edgeIndex = diagram.edges.findIndex((e) => e.fromId == fromNodeId && e.toId == toNodeId);
    selectedEdge.value = diagram.edges[edgeIndex];
    if (useSideNavStore().visible) {
      useSideNavStore().hide();
      tempNavHidden = true;
    }
  };
  window.nodeDoubleClick = function (nodeId) {
    fromNodeId.value = null;
    selectedNodeId.value = nodeId;
    selectedNode.value = diagram.nodes[nodeId];
    if (useSideNavStore().visible) {
      useSideNavStore().hide();
      tempNavHidden = true;
    }
  };
  window.nodeClick = function (nodeId) {
    console.log("callback: " + nodeId);
    if (fromNodeId.value) {
      diagram.createEdge(fromNodeId.value, nodeId);
      fromNodeId.value = null;
    } else {
      fromNodeId.value = nodeId;
    }
  };

});

onUnmounted(() => {
  window.removeEventListener("keydown", escapeKeyHandler);
});

async function addNode() {
  diagram.createNode(addNodeLabel.value, addNodeLogicModel.value);
  addNodeLabel.value = "";
  // now put focus on the input element with id 'addNodeLabel'
  document.getElementById('addNodeLabel').focus();
}

function removeFromEdge(array, value) {
  const index = array.findIndex((item) => item.toId === value);
  if (index !== -1) {
    array.splice(index, 1);
  }
  return array;
}

function removeToEdge(array, value) {
  const index = array.findIndex((item) => item.fromId === value);
  if (index !== -1) {
    array.splice(index, 1);
  }
  return array;
}

function deleteConnection(fromId, toId) {
  const index = diagram.edges.findIndex(
    (edge) => edge.fromId === fromId && edge.toId === toId
  );
  diagram.edges.splice(index, 1);

  const key = `${fromId}|${toId}`;
  diagram.edgeSet.delete(key);

  drawDiagram();
  // reset select dropdown and disable the delete button
  deleteFromId.value = deleteToId.value = null;
  selectedEdge.value = null; // closes modal (needed if coming from edge Modal)
}

function deleteNode(nodeId) {
  // remove edges
  let i = 0;
  while (diagram.edges[i]) {
    console.log(i);
    if (diagram.edges[i].fromId === nodeId || diagram.edges[i].toId === nodeId) {
      diagram.edges.splice(i, 1);
      i--;
    }
    i++;
  }
  delete diagram.nodes[nodeId];
  selectedNodeId.value = null; // closes modal
  drawDiagram();
}

const getJSON = () => {
  console.log(diagram.toJSON(diagram.nodes, diagram.edges));
};

const uploadDiagram = async function () {
  await getUploadUrl(diagramContainer.value.innerHTML);
};

async function getUploadUrl(svgElement) {
  console.log(svgElement);
  // URL for the AWS API Gateway that returns a pre-signed URL and filename for uploading to S3.
  const s3uploaderUrl = "https://238xuirz88.execute-api.us-west-2.amazonaws.com/uploads";

  // URL to download the file after it it uploaded
  const downloadUrl = "https://sbc-upload.s3.us-west-2.amazonaws.com/";

  // Pass the content type as a query parameter
  const contentType = "image/svg+xml"; // or  'image/svg';

  axios
    .get(s3uploaderUrl, {
      params: {
        contentType: contentType,
      },
    })
    .then((response) => {
      console.log("Signed URL:", response.data.uploadURL);
      console.log("Key:", response.data.Key);
      svgUrl.value = downloadUrl + response.data.Key;

      // This is the SVG file you want to upload. In a web app,
      // you can get this from an input field, for example.
      const svgBlob = new Blob([svgElement], { type: contentType });

      // Perform the actual upload using the signed URL
      return axios.put(response.data.uploadURL, svgBlob, {
        headers: {
          "Content-Type": contentType,
        },
      });
    })
    .then((response) => {
      console.log("Upload successful!");
      // now that it's uploaded, we can update the img tag's src attribute
      svgImgSrcUrl.value = svgUrl.value;
    })
    .catch((error) => console.error("Error:", error));
}

function rotateDiagram() {
  diagram.rotate();
  drawDiagram();
}

const closeModal = () => {
  selectedNodeId.value = null;
  selectedEdge.value = null;
  showIndicatorModal.value = false;

  // if (tempNavHidden) {
  //   tempNavHidden = false;
  // }

  useSideNavStore().show();
  drawDiagram();
};

const modalRef = ref(null);
const edgeModalRef = ref(null);

onClickOutside(modalRef, closeModal);
onClickOutside(edgeModalRef, closeModal);

const escapeKeyHandler = (event) => {
  if (event.key === "Escape" || event.keyCode === 27) {
    closeModal();
  }
};

const loadExampleToc = async (filename) => {
  try {
    const response = await fetch(`/tocs/${filename}.json`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const jsonText = await response.text();
    console.log("here we go");
    console.log(jsonText);
    diagram.parseJSON(jsonText);
  } catch (error) {
    console.error('Failed to fetch JSON data:', error);
  }
}
</script>

<template>
  <div class="mx-3">

    <TheoryOfChangeItemModalVue :is-new="modalConfig.isItemNew" :is-visible="modalConfig.isVisible"
      :theory-of-change-id="modalConfig.theoryOfChangeId"
      @is-closed="modalConfig.isVisible = false; modalConfig.theoryOfChangeId = undefined"
      @on-item-added="diagram.parseGraph($event)" v-if="modalConfig.isVisible === true">
    </TheoryOfChangeItemModalVue>

    <div class="columns">
      <div class="column">
        <!-- TODO: change id -->
        <button
          @click.prevent="modalConfig.isItemNew = true; modalConfig.isVisible = true; modalConfig.theoryOfChangeId = 1">Add
          Item</button>
      </div>

      <div class="column">
        <button>Logical View</button>
        <button>Rotate</button>
      </div>

    </div>

    <div class="mt-4 container">
      <p>Content here</p>
    </div>
  </div>
</template>

<style>
.custom-flex-container {
  display: flex;
  align-items: flex-end;
}

.custom-control {
  display: flex;
  flex-direction: column-reverse;
  align-items: flex-end;
}

.buttons-container {
  position: absolute;
  top: 20px;
  right: 10px;
}

.button-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding-bottom: calc(0.5em + 0.25rem);
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
}

input:checked+.slider {
  background-color: #3f51b5;
}

input:checked+.slider:before {
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>



<!--
        <div class="field">
          <div class="control">
            <div>
              <button class="button is-info" type="button" @click="uploadDiagram">
                Upload
              </button>
            </div>
          </div>
        </div>
        <div class="field">
          <div class="control">
            <div>
              <button class="button is-info" type="button" @click="getJSON">
                Download JSON
              </button>
            </div>
          </div>
        </div>
-->



        <!-- <div class="field" v-if="true">
          <label class="label">JSON String to Import</label>
          <div class="control">
            <input
              class="input"
              @change="diagram.parseJSON(textToImport)"
              type="text"
              name="importNode"
              id="importNode"
              v-model="textToImport"
            />
          </div>
        </div> -->
