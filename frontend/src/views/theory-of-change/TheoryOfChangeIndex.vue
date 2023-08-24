<script lang="ts" setup>
import mermaid from "mermaid";

import { onMounted, onUnmounted, reactive, ref, computed } from "vue";
import { Risk, SEMS, THEORY_OF_CHANGE_TYPES, TheoryOfChange } from "@/types";
import {
  Button,
  Card,
  Divider,
  Form,
  FormItem,
  Input,
  Modal,
  Space,
  Spin,
  Switch,
  Textarea,
} from "ant-design-vue";
import TheoryOfChangeExamplesBrowser from "./TheoryOfChangeExamplesBrowser.vue";
import TheoryOfChangeItemModal from "./TheoryOfChangeItemModal.vue";
import RiskModal from "./RiskModal.vue";
import {
  DeleteOutlined,
  PlusCircleOutlined,
  RotateRightOutlined,
  SwapLeftOutlined,
  SwapOutlined,
} from "@ant-design/icons-vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { uploadListProps } from "ant-design-vue/es/upload/interface";

const showIndicatorModal = ref(false);
const theoryOfChangeModel = ref<{
  data: TheoryOfChange[];
  selectedItem: TheoryOfChange;
}>({
  data: [],
  selectedItem: new TheoryOfChange(),
});
const tocItemModalConfig = ref({
  visible: false,
  toc: new TheoryOfChange(),
});

const store = useTheoryOfChangeStore();

const diagramContainer = ref(null);
const fromNodeId = ref(null);
const selectedNodeId = ref(null);
const selectedEdge = ref(null);
const selectedNode = ref(null);
const logicModelView = ref(false);

const config = reactive({
  isLoading: true,
  isExamplePanelVisible: false,
});

// === START: Risks Modal functions
const risksModalConfig = ref({
  visible: false,
  risk: {
    toc_from_id: null,
    toc_to_id: null,
  },
});

function showRiskModal(edge?: { fromId?: number; toId?: number }) {
  if (edge == null) {
    return;
  }

  risksModalConfig.value.risk = {
    toc_from_id: edge.fromId,
    toc_to_id: edge.toId,
  };
  risksModalConfig.value.visible = true;
}
function closeRiskModal() {
  risksModalConfig.value.visible = false;
  risksModalConfig.value.risk = {
    toc_from_id: null,
    toc_to_id: null,
  };
}
// === END: Risks Modal functions

const mermaidConfig = {
  startOnLoad: true,
  securityLevel: "loose",
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
  // if (diagramContainer.value == null) {
  //   return;
  // }

  const { svg } = await mermaid.render("graphDiv", diagram.toMermaid());
  diagramContainer.value.innerHTML = "";
  const svgWrapper = document.createElement("div");
  svgWrapper.innerHTML = svg;
  const svgElement = svgWrapper.firstChild;
  diagramContainer.value.appendChild(svgElement);

  // Add click event listeners to the nodes manually
  const nodes = diagramContainer.value.querySelectorAll(".node");
  nodes.forEach((node) => {
    let clickTimeout: any;
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
};

function nodesToSubgraph(nodes: Object, category: string) {
  category = category.toLowerCase();
  let result = "";
  const arrayInCategory = Object.fromEntries(
    Object.entries(nodes).filter(([, node]) => node.logicModel.toLowerCase() == category)
  );
  if (Object.keys(arrayInCategory).length) {
    result += "subgraph " + (category == "" ? "no category" : category) + "\n";
    for (const key in arrayInCategory) {
      result += `${nodes[key].id}["${nodes[key].label}"]\n`;
    }
    result += "end\n";
  }
  return result;
}

function Node(id: number | string, label: string, defaultProperties: Object) {
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

function Edge(fromNodeId: number, toNodeId: number) {
  this.fromId = fromNodeId;
  this.toId = toNodeId;
}

const diagram = reactive({
  defaultNode: {
    id: "",
    label: "",
    name: "",
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
    risks: "",
  },
  diagramType: "flowchart",
  orientationIndex: 0,
  orientationOptions: ["LR", "TB", "RL", "BT"],
  nextNodeId: "Aa",
  nodes: {},
  edges: [],
  edgeSet: new Set(),

  edgeLabel(edge, fromOrTo) {
    if (edge == null) return;

    if (fromOrTo == "from") {
      return this.nodes[edge.fromId]?.label || "N/A";
    }
    return this.nodes[edge.toId]?.label || "N/A";
  },
  orientation: function () {
    return this.orientationOptions[this.orientationIndex];
  },
  rotate: function () {
    this.orientationIndex++;
    if (this.orientationIndex == 4) this.orientationIndex = 0;
  },
  parseGraph: function (data: TheoryOfChange[]) {
    theoryOfChangeModel.value.data = data;

    this.nodes = {};
    this.edges = [];
    this.edgeSet = new Set();

    const graph = data.map((r: TheoryOfChange) => {
      return {
        id: r.id,
        label: r.name,
        // name: r.name,
        description: r.description,
        validated: false,
        // validated: r.validated,
        // indicator: r.indicators,
        sem: SEMS[`${r.sem_id?.toString()}`],
        logicModel: THEORY_OF_CHANGE_TYPES[`${r.type_id}`],
        audience: [] as any,
      };
    });

    for (const node of graph) {
      // Merge the input object with the default node, so any missing properties are filled in
      const mergedNode = Object.assign({}, this.defaultNode, node);
      this.nodes[mergedNode.id] = mergedNode;
    }

    const edges: {
      fromId: number;
      toId: number;
      // assumptions: any;
      // risks: any;
    }[] = data.flatMap((r) => {
      if ((r.links_to || []).length == 0) {
        return { fromId: r.id, toId: null };
      }

      return r.links_to.flatMap((l) => {
        return { fromId: r.id, toId: l };
      });
    });

    for (const edge of edges) {
      this.createEdge(edge.fromId, edge.toId, false);
    }
    drawDiagram();
  },

  createNode: function (label: string, logicModel: string) {
    const node = Node(this.nextNodeId, label, this.defaultNode);
    node.logicModel = logicModel;
    this.nodes[this.nextNodeId] = node;
    this.nextNodeId =
      String.fromCharCode(this.nextNodeId.charCodeAt(0) + 1) + this.nextNodeId.charAt(1);

    drawDiagram();
    return node;
  },

  createEdge: function (fromNodeId, toNodeId, draw = true) {
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
        result += `${this.nodes[key].id}["${this.nodes[key].label}"]\n`;
      }
    }
    for (const edge of this.edges) {
      if (edge.fromId && edge.toId) {
        result += `${edge.fromId} -->|risk factors| ${edge.toId}\n`;
      }
    }
    return result;
  },
  toJSON: function (inputNodes, edges) {
    const nodes = Object.values(inputNodes);
    return JSON.stringify({ nodes, edges });
  },
});

const fetchGraph = async () => {
  config.isLoading = true;
  store
    .download()
    .then(() => {
      diagram.parseGraph(store.theory_of_change);
    })
    .finally(() => (config.isLoading = false));
};

const escapeKeyHandler = (event) => {
  if (event.key === "Escape" || event.keyCode === 27) {
    tocItemModalClosed();
  }
};

onMounted(() => {
  fetchGraph();

  mermaid.initialize(mermaidConfig);

  window.addEventListener("keydown", escapeKeyHandler);

  // @ts-ignore
  window.edgeDoubleClick = function (fromNodeId: number, toNodeId: number) {
    showRiskModal({ fromId: fromNodeId, toId: toNodeId });
  };

  window.nodeDoubleClick = function (nodeId) {
    fromNodeId.value = null;
    selectedNodeId.value = nodeId;
    selectedNode.value = diagram.nodes[nodeId];

    theoryOfChangeModel.value.selectedItem = theoryOfChangeModel.value.data.find(
      (item: any) => item.id == nodeId
    );

    const selectedItem = theoryOfChangeModel.value.selectedItem;
    if (selectedItem != null) {
      console.log(selectedItem);
      tocItemModalConfig.value.toc = selectedItem;
      tocItemModalConfig.value.visible = true;
    }
  };
  window.nodeClick = function (nodeId) {
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

function deleteNode(nodeId: number) {
  // remove edges
  let i = 0;
  while (diagram.edges[i]) {
    if (diagram.edges[i].fromId == nodeId || diagram.edges[i].toId == nodeId) {
      diagram.edges.splice(i, 1);
      i--;
    }
    i++;
  }

  delete diagram.nodes[nodeId];
  selectedNodeId.value = null; // closes modal
  drawDiagram();
}

function rotateDiagram() {
  diagram.rotate();
  drawDiagram();
}

//=== START: Theory of Change Item Modal functions
const newTocItem = () => {
  tocItemModalConfig.value.toc = new TheoryOfChange();
  tocItemModalConfig.value.visible = true;
};

const tocItemModalClosed = (redraw = true, data?: TheoryOfChange[]) => {
  selectedNodeId.value = null;
  showIndicatorModal.value = false;

  tocItemModalConfig.value.visible = false;
  tocItemModalConfig.value.toc = new TheoryOfChange();

  if (data != null) {
    diagram.parseGraph(data);
  }

  if (redraw) {
    drawDiagram();
  }
};

//=== END: Theory of Change Item Modal functions
</script>

<template>
  <Card title="Theory of Change" :bordered="false" :loading="config.isLoading">
    <!-- Theory of Change Item Modal -->
    <TheoryOfChangeItemModal
      :visible="tocItemModalConfig.visible"
      :toc="tocItemModalConfig.toc"
      @closed="tocItemModalClosed(false)"
      @saved="tocItemModalClosed(false, $event)"
      @deleted="deleteNode($event)"
    ></TheoryOfChangeItemModal>

    <!-- Risk Modal -->
    <RiskModal
      :visible="risksModalConfig.visible"
      @close="closeRiskModal()"
      :edge="risksModalConfig.risk"
    ></RiskModal>

    <!-- Theory of Change examples browser panel -->
    <TheoryOfChangeExamplesBrowser
      :is-visible="config.isExamplePanelVisible"
      @is-closed="config.isExamplePanelVisible = false"
      v-if="config.isExamplePanelVisible"
    >
    </TheoryOfChangeExamplesBrowser>

    <div v-if="!config.isLoading">
      <div class="level">
        <div class="level-item has-text-centered">
          <Button type="primary" class="mr-6" @click="newTocItem()">
            <template #icon>
              <PlusCircleOutlined />
            </template>
            Add Item
          </Button>

          <Button type="ghost" shape="round" @click="rotateDiagram()">
            <template #icon>
              <RotateRightOutlined />
            </template>
            Rotate
          </Button>

          <Switch
            v-model:checked="logicModelView"
            checked-children="Logic Model View"
            un-checked-children="Normal View"
            class="ml-3"
            @change="drawDiagram"
          />
        </div>

        <!-- <Space>
          <span>
            Need help?
            <Button
              style="padding-left; 0px; margin-left: 0px; display: inline"
              type="link"
              @click="config.isExamplePanelVisible = true"
              >Browse theory of change examples</Button
            >
          </span>
        </Space> -->
      </div>

      <Divider></Divider>

      <div class="mt-4">
        <div
          class="diagram-container"
          ref="diagramContainer"
          style="display: flex; width: 100%"
        ></div>
      </div>
    </div>
  </Card>
</template>

<style></style>
