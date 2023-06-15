<script lang="ts"  setup>
// @ts-ignore
// import mermaidAPI from "/node_modules/mermaid/dist/mermaid.esm.mjs";
import mermaid from 'mermaid';

import { onMounted, onUnmounted, reactive, ref, computed } from "vue";
import { useSideNavStore } from "@/stores/sideNav";
import axios from "axios";
import { onClickOutside } from "@vueuse/core";
import IndicatorBrowserPanel from "./IndicatorBrowserPanel.vue";
import { ApiRequest } from "@/apis/api";
import { Risk, TheoryOfChange, TheoryOfChangeItem } from "@/types";
import GridLoader from "@/components/spinners/GridLoader.vue";
import { useProjectDataStore } from "@/stores/projectData";
import { useProjectStore } from '@/stores/projects';
import { Button, Divider, Form, FormItem, Input, Modal, Space, Spin, Switch, Textarea } from "ant-design-vue";
import TheoryOfChangeExamplesBrowser from "./TheoryOfChangeExamplesBrowser.vue";
import { PlusCircleOutlined, RotateRightOutlined, SwapLeftOutlined, SwapOutlined } from "@ant-design/icons-vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";

const THEORY_OF_CHANGE_TYPES: Record<string, string> = {
  "1": "Input",
  "2": "Activity",
  "3": "Output",
  "4": "Outcome",
  "5": "Impact",
}

const SEMS: Record<string, string> = {
  "1": "Individual",
  "2": "Interpersonal",
  "3": "Community",
  "4": "Organizational",
  "5": "Policy/Enabling environment",
}

const isPanelVisible = ref(false);
const showIndicatorModal = ref(false);
const theoryOfChangeModel = ref<{
  data: TheoryOfChange[],
  selectedItem: TheoryOfChange
}>({
  data: [],
  selectedItem: new TheoryOfChange()
}),
  tocItemModalConfig = ref({
    visible: false,
    itemId: null,
    data: {},
    isNew: false,
    theoryOfChangeId: null,
    isLoading: false,
    isDeleting: false,
    form: new TheoryOfChange()
  }),
  config = reactive({
    isLoading: true,
    isExamplePanelVisible: false,
  });

const projectStore = useProjectStore(),
  theoryOfChangeStore = useTheoryOfChangeStore();

const diagramContainer = ref(null);
const fromNodeId = ref(null);
const selectedNodeId = ref(null);
const selectedEdge = ref(null);
const selectedNode = ref(null);
const logicModelView = ref(false);


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
  const { svg } = await mermaid.render("graphDiv", diagram.toMermaid());
  if (diagramContainer.value) {
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
  }
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
      result += `${nodes[key].id}[${nodes[key].label}]\n`;
    }
    result += "end\n";
  }
  return result;
}

function Node(id: number, label: string, defaultProperties: Object) {
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
  parseGraph: function (data: TheoryOfChange[]) {
    console.log(data)
    // if (Array.isArray(data)) data = data[0]

    theoryOfChangeModel.value.data = data;

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
      }
    });

    for (const node of graph) {
      // Merge the input object with the default node, so any missing properties are filled in
      const mergedNode = Object.assign({}, this.defaultNode, node);
      this.nodes[mergedNode.id] = mergedNode;
    }

    const edges: {
      fromId: number;
      toId: number;
      assumptions: any;
      risks: any;
    }[] = [];

    for (const r of data) {
      edges.push({
        fromId: r.id,
        toId: r.to_id,
        assumptions: r.assumptions,
        risks: r.risks
      })

      if (r.from_id != null) {
        edges.push({
          fromId: r.from_id,
          toId: r.id,
          assumptions: r.assumptions,
          risks: r.risks
        });
      }
    }

    for (const edge of edges) {
      this.createEdge(edge.fromId, edge.toId, false);
    }
    drawDiagram();
  },

  createNode: function (label, logicModel) {
    const node = new Node(this.nextNodeId, label, this.defaultNode);
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
        result += `${this.nodes[key].id}[${this.nodes[key].label}]\n`;
      }
    }
    for (const edge of this.edges) {
      result += `${edge.fromId} -->|factors| ${edge.toId}\n`;
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
  theoryOfChangeStore.fetchTheoryOfChange()
    .then(() => {
      diagram.parseGraph(theoryOfChangeStore.theory_of_change);
    })
    .finally(() => config.isLoading = false);
}

const escapeKeyHandler = (event) => {
  if (event.key === "Escape" || event.keyCode === 27) {
    closeModal();
  }
};

onMounted(() => {
  fetchGraph()

  mermaid.initialize(mermaidConfig);

  window.addEventListener("keydown", escapeKeyHandler);

  window.edgeDoubleClick = function (fromNodeId, toNodeId) {
    const edgeIndex = diagram.edges.findIndex((e) => e.fromId == fromNodeId && e.toId == toNodeId);

    selectedEdge.value = diagram.edges[edgeIndex];
    risksModalConfig.form.toc_from_id = fromNodeId;
    risksModalConfig.form.toc_to_id = toNodeId;
    risksModalConfig.showModal()
  };
  window.nodeDoubleClick = function (nodeId) {
    fromNodeId.value = null;
    selectedNodeId.value = nodeId;
    selectedNode.value = diagram.nodes[nodeId];

    theoryOfChangeModel.value.selectedItem = theoryOfChangeModel.value.data.find((item: any) => item.id == nodeId);

    const selectedItem = theoryOfChangeModel.value.selectedItem as any;
    if (selectedItem != null) {
      tocItemModalConfig.value.isNew = false;
      tocItemModalConfig.value.form = selectedItem;
      tocItemModalConfig.value.itemId = selectedItem.id;
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

function deleteNode(nodeId) {
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

  tocItemModalConfig.value.form = new TheoryOfChange()
  tocItemModalConfig.value.isNew = true;
  tocItemModalConfig.value.theoryOfChangeId = 1;
  tocItemModalConfig.value.visible = true;
  useSideNavStore().hide();
}

const closeModal = (redraw = true) => {
  selectedNodeId.value = null;
  selectedEdge.value = null;
  showIndicatorModal.value = false;

  tocItemModalConfig.value.visible = false;
  tocItemModalConfig.value.form = new TheoryOfChange();

  // useSideNavStore().show();
  if (redraw) {
    drawDiagram();
  }
};

const saveFormItem = async () => {
  // TODO: send response as callback to close the form
  const fields = tocItemModalConfig.value.form,
    tocId = theoryOfChangeModel.value.data;

  const data = {
    name: fields.name,
    type_id: fields.type_id,
    from_id: fields.from_id,
    to_id: fields.to_id,
    sem_id: fields.sem_id,
    description: fields.description,
    is_validated: fields.is_validated || false
  };

  tocItemModalConfig.value.isLoading = true;
  if (tocItemModalConfig.value.itemId != null || !tocItemModalConfig.value.isNew) {
    // Update item
    await ApiRequest.put<TheoryOfChange>(`theory-of-change/${projectStore.prj_id}/item/${tocItemModalConfig.value.itemId}`, data)
      .then(resp => {
        diagram.parseGraph(resp);
        closeModal(false);
      }).finally(() => {
        tocItemModalConfig.value.isLoading = false;
      });
  } else {
    //  Create item
    await ApiRequest.post<TheoryOfChange>(`theory-of-change/${projectStore.prj_id}/item`, data)
      .then(resp => {
        diagram.parseGraph(resp);

        closeModal(false);
      }).finally(() => {
        tocItemModalConfig.value.isLoading = false;
      });
  }

}

function deleteItem() {
  tocItemModalConfig.value.isDeleting = true;

  const tocId = theoryOfChangeModel.value.data.id;
  ApiRequest.delete(`theory-of-change/${tocId}/item/${tocItemModalConfig.value.itemId}`)
    .then(_ => {
      deleteNode(selectedNodeId.value);

      closeModal(false);
    }).finally(() => {
      tocItemModalConfig.value.isDeleting = false;
    });
}

function updateToCModel(resp: TheoryOfChange | TheoryOfChange[], itemId?: number) {
  if (Array.isArray(resp)) {
    resp = resp[0];
  }

  theoryOfChangeModel.value.data = resp;
  if (itemId != null) {
    theoryOfChangeModel.value.selectedItem = resp.graph.find(i => i.id == itemId);
  }
}
//=== END: Theory of Change Item Modal functions


// === START: Risks Modal functions
const risksModalConfig = reactive({
  visible: false,
  isSaving: false,
  form: new Risk(),
  showModal: () => {
    const edge = selectedEdge?.value;
    if (edge == null) {
      return
    }
    const toc = theoryOfChangeModel.value?.data
    if (toc == null) {
      return;
    }

    const existingRisk = toc.risks.find(i => i.toc_from_id == edge.fromId && i.toc_to_id == edge.toId)
    risksModalConfig.form = existingRisk ?? new Risk();
    risksModalConfig.visible = true;
  },
  closeModal: () => {
    risksModalConfig.visible = false;
    risksModalConfig.form = new Risk();
  },
  saveForm: async () => {
    const tocId = theoryOfChangeModel.value?.data?.id;
    if (tocId == null) {
      return;
    }

    const data = {
      name: risksModalConfig.form.name,
      assumptions: risksModalConfig.form.assumptions,
      risks: risksModalConfig.form.risks,
      toc_to_id: risksModalConfig.form.toc_to_id,
      toc_from_id: risksModalConfig.form.toc_from_id ?? undefined,
    };

    risksModalConfig.isSaving = true;
    await ApiRequest.post(`theory-of-change/${tocId}/risks`, data)
      .then(resp => {
        diagram.parseGraph(resp);
        risksModalConfig.closeModal();
      }).finally(() => {
        risksModalConfig.isSaving = false;
      });
  }
});
// === END: Risks Modal functions
</script>

<template>
  <section class="section">
    <div v-if="config.isLoading" id="graph-loader" style="margin-top: auto;">
      <GridLoader :use-logo="false" :loading="config.isLoading"></GridLoader>
    </div>

    <div class="mx-3" v-if="!config.isLoading">

      <!-- Indicator Browser Panel -->
      <IndicatorBrowserPanel :is-visible="isPanelVisible"
        @is-closed="isPanelVisible = false; showIndicatorModal = true; useSideNavStore().hide();"
        :toc-item="theoryOfChangeModel.selectedItem"
        @is-saved="updateToCModel($event, theoryOfChangeModel.selectedItem?.id)">
      </IndicatorBrowserPanel>

      <!-- Theory of Change examples browser panel -->
      <TheoryOfChangeExamplesBrowser :is-visible="config.isExamplePanelVisible"
        @is-closed="config.isExamplePanelVisible = false" v-if="config.isExamplePanelVisible">
      </TheoryOfChangeExamplesBrowser>


      <div class="level">
        <div class="level-item has-text-centered">

          <Button type="primary" class="mr-6" @click.prevent="newTocItem()">
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

          <Switch v-model:checked="logicModelView" checked-children="Logic Model View" un-checked-children="Normal View"
            class="ml-3" @change="drawDiagram" />

        </div>

        <Space>
          <span>
            Need help? <Button style="padding-left; 0px; margin-left: 0px; display: inline" type="link"
              @click="config.isExamplePanelVisible = true;">Browse theory of change examples</Button>
          </span>
        </Space>
      </div>

      <Divider></Divider>

      <!-- ======== START: Theory of Change Modal ======= -->
      <Modal v-model:visible="tocItemModalConfig.visible" @ok="closeModal()">
        <template #footer>
          <footer style="display: block;">
            <div class="level">
              <div class="level-left">
                <div class="level-item">
                  <button role="button" class="button is-small is-danger" @click="deleteItem()"
                    v-if="tocItemModalConfig.isNew == false"
                    :class="{ 'is-loading disabled': tocItemModalConfig.isDeleting }"
                    :disabled="tocItemModalConfig.isDeleting">
                    <span class="icon mr-1">
                      <i class="fas fa-trash"></i>
                    </span>
                    Delete
                  </button>

                </div>
              </div>

              <div class="level-right">
                <div class="level-item">
                  <button class="button is-primary" :class="{ 'is-loading': tocItemModalConfig.isLoading }"
                    :disabled="tocItemModalConfig.isLoading" role="button" @click.prevent="saveFormItem()">
                    {{ tocItemModalConfig.isNew ? 'Save' : 'Update' }}
                  </button>

                  <button class="button" role="button" @click="closeModal">Cancel</button>
                </div>
              </div>
            </div>
          </footer>
        </template>

        <form>
          <div class="field">
            <div class="field-body">
              <div class="field">
                <div class="control">
                  <label class="label">Label</label>
                  <input class="input" type="text" maxlength="80" v-model="tocItemModalConfig.form.name" />
                </div>
              </div>
            </div>
          </div>

          <div class="field is-horizontal">
            <div class="columns field-body">

              <div class="column field">
                <label class="label">Links From</label>

                <div class="control">
                  <div class="select is-fullwidth">
                    <!-- TODO: show list of existing indicators -->
                    <select v-model="tocItemModalConfig.form.from_id">

                      <option v-for="item in theoryOfChangeModel?.data?.graph" :key="item.id" :value="item.id">
                        {{ item.name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="column field">
                <label class="label">Links To</label>

                <div class="control">
                  <div class="select is-fullwidth">
                    <!-- TODO: show list of existing indicators -->
                    <select v-model="tocItemModalConfig.form.to_id">
                      <option v-for="item in theoryOfChangeModel?.data?.graph" :key="item.id" :value="item.id">
                        {{ item.name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="field is-horizontal">
            <div class="columns field-body">
              <!-- Column 1: SEM Level and Category -->
              <div class="column field">
                <label class="label">Logic Model Category</label>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="tocItemModalConfig.form.type_id">
                      <option v-for="key in Object.keys(THEORY_OF_CHANGE_TYPES)" :key="key" :value="key">
                        {{ THEORY_OF_CHANGE_TYPES[key] }}
                      </option>

                    </select>
                  </div>
                </div>
              </div>

              <!-- Column 2: Audience -->
              <div class="column field">
                <label class="label">SEM Level</label>

                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="tocItemModalConfig.form.sem_id">
                      <option v-for="key in Object.keys(SEMS)" :key="key" :value="key">
                        {{ SEMS[key] }}
                      </option>

                    </select>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <div class="field">
            <div class="control">
              <label class="label">
                Validated
                <input type="checkbox" class="ml-3" v-model="tocItemModalConfig.form.is_validated" />
              </label>
            </div>
          </div>


          <div class="field">
            <label class="label">Description</label>
            <div class="control">
              <textarea class="textarea" rows="4" columns="80" maxlength="999"
                v-model="tocItemModalConfig.form.description" />
            </div>
          </div>


          <!-- TODO: implement saving of indicators -->
          <div class="field">
            <label class="label">Indicators</label>

            <hr>

            <div class="field is-grouped is-grouped-multiline">
              <div class="control" v-for="item in theoryOfChangeModel.selectedItem?.indicators" :key="item.id">
                <div class="tags has-addons">
                  <a class="tag is-link">{{ item.indicator.name }}</a>
                  <a class="tag is-delete"></a>

                  <!-- TODO: implement deleting of item -->
                </div>
              </div>
            </div>

            <button class="button is-small" role="button"
              @click.prevent="isPanelVisible = !isPanelVisible; showIndicatorModal = true; useSideNavStore().hide();">
              <span class="icon is-small mr-1">
                <i class="fas fa-plus"></i>
              </span>
              Add Indicator
            </button>
          </div>

        </form>
      </Modal>
      <!-- ======== END: Theory of Change Modal ======= -->


      <!-- ======== START: Risks Modal ======= -->
      <Modal v-model:visible="risksModalConfig.visible" @ok="risksModalConfig.closeModal()">

        <template #title>
          <span>
            {{ diagram.edgeLabel(selectedEdge, 'from') }}
            <SwapOutlined />
            {{ diagram.edgeLabel(selectedEdge, 'to') }}
          </span>
        </template>

        <template #footer>
          <footer style="display: block;">
            <Button :disabled="risksModalConfig.isSaving" @click="risksModalConfig.closeModal()">Cancel</Button>

            <Button :loading="risksModalConfig.isSaving" @click="risksModalConfig.saveForm()" type="primary">Save</Button>
          </footer>
        </template>

        <Form layout="vertical" :model="risksModalConfig.form">
          <Spin :spinning="risksModalConfig.isSaving">
            <FormItem label="Name">
              <Input v-model:value="risksModalConfig.form.name" placeholder="" />
            </FormItem>

            <FormItem label="Assumptions">
              <Textarea v-model:value="risksModalConfig.form.assumptions" placeholder="" />
            </FormItem>

            <FormItem label="Risks">
              <Textarea v-model:value="risksModalConfig.form.risks" placeholder="" />
            </FormItem>
          </Spin>
        </Form>
      </Modal>
      <!-- ======== END: Risks Modal ======= -->


      <!-- TODO: add edge modal -->


      <div class="mt-4">
        <div class="diagram-container" ref="diagramContainer" style="display: flex; width: 100%;"></div>
      </div>
    </div>
  </section>
</template>

<style>
#graph-loader {
  position: fixed;
  top: 50%;
  left: 50%;
  /* bring your own prefixes */
  transform: translate(-50%, -50%);
}
</style>
