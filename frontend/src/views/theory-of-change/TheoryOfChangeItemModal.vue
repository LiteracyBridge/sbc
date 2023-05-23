<script lang="ts"  setup>
// @ts-ignore
import mermaidAPI from "/node_modules/mermaid/dist/mermaid.esm.mjs";
import { onMounted, onUnmounted, reactive, ref, computed } from "vue";
import { useSideNavStore } from "@/stores/sideNav";
import axios from "axios";
import { onClickOutside } from "@vueuse/core";
import IndicatorBrowserPanel from "@/components/IndicatorBrowserPanel.vue";
import { ApiRequest } from "@/apis/api";

const form = ref<{
  name: string; type: string | number,
  sem: string | number,
  is_validated: boolean,
  description: string,
  to_id?: number | number,
  from_id?: number | number,
}>({
  name: undefined,
  type: undefined,
  sem: undefined,
  description: undefined,
  is_validated: false,
  to_id: undefined,
  from_id: undefined,
});
const config = ref({ isLoading: false });


const isPanelVisible = ref(false);
const showIndicatorModal = ref(false);

const svgUrl = ref("");
const svgImgSrcUrl = ref("");
const diagramContainer = ref(null);
const addNodeLabel = ref("");
const addNodeLogicModel = ref("");
const fromNodeId = ref(null);
const selectedNodeId = ref(null);
const selectedEdge = ref(null);


const emit = defineEmits(['onItemAdded', 'isClosed']);

const props = defineProps({
  isNew: {
    type: Boolean,
    required: true,
  },
  theoryOfChangeId: {
    type: Number,
    required: false,
  },
  isVisible: {
    type: Boolean,
    required: true,
  },
  items: {
    type: Array,
    required: false,
    default: []
  },
});

const getItems = computed<{ name: string; id: number }[]>(() => {
  return props.items as { name: string; id: number }[];
});

const closeModal = () => {

  selectedNodeId.value = null;
  selectedEdge.value = null;
  showIndicatorModal.value = false;

  // if (tempNavHidden) {
  //   tempNavHidden = false;
  // }

  emit("isClosed", true);
  useSideNavStore().show();
  // drawDiagram();
};

const saveForm = async () => {
  // TODO: make http request to save the form
  // TODO: send response as callback to close the form
  const fields = form.value;

  config.value.isLoading = true;
  await ApiRequest.post(`theory-of-change/${props.theoryOfChangeId}/item`, {
    name: fields.name,
    type_id: 1,
    from_id: fields.from_id,
    to_id: fields.to_id,
    sem_id: 1,
    description: "dummy description"
  }).then(resp => {
    console.log(resp)

    emit("onItemAdded", resp);
    closeModal();
  }).finally(() => {
    config.value.isLoading = false;
  });
}

function deleteItem() {
  // TODO: implement deleting of the item
  // remove edges
}


onMounted(() => {
  if (props.isVisible) {
    useSideNavStore().hide();
  }
  // drawDiagram();
});
const modalRef = ref(null);
const edgeModalRef = ref(null);

onClickOutside(modalRef, closeModal);
onClickOutside(edgeModalRef, closeModal);

</script>

<template>
  <div>

    <div class="`modal p-2`" :class="{ 'is-active': props.isVisible }">
      <div class="modal-background"></div>

      <div ref="modalRef" class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Theory of Change Item</p>
          <button @click="closeModal" class="delete" aria-label="close"></button>
        </header>

        <section class="modal-card-body">
          <form>

            <!-- <div class="level-left is-normal">
              <label class="label">Label</label>
            </div> -->
            <div class="field">
              <div class="field-body">
                <div class="field">
                  <div class="control">
                    <label class="label">Label</label>
                    <input class="input" type="text" maxlength="80" v-model="form.name" />
                  </div>
                </div>
              </div>
              <!-- <div class="level-right">
                <div class="level-item">
                  <button class="button is-danger ml-6" @click="deleteNode(selectedNodeId)">
                    Delete
                  </button>
                </div>
              </div> -->
            </div>

            <div class="field is-horizontal">
              <div class="field-body">

                <div class="field">
                  <label class="label">Links From</label>

                  <div class="control">
                    <div class="select is-fullwidth">
                      <!-- TODO: show list of existing indicators -->
                      <select v-model="form.from_id">
                        <!-- @ts-ignore -->
                        <option v-for="item in getItems" :key="item.id" :value="item.id">
                          {{ item.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>

                <div class="field">
                  <label class="label">Links To</label>

                  <div class="control">
                    <div class="select is-fullwidth">
                      <!-- TODO: show list of existing indicators -->
                      <select v-model="form.to_id">
                        <!-- @ts-ignore -->
                        <option v-for="item in getItems" :key="item.id" :value="item.id">
                          {{ item.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>


            <div class="field is-horizontal">
              <div class="field-body">
                <div class="columns">
                  <!-- Column 1: SEM Level and Category -->

                  <div class="column">
                    <div class="field">
                      <label class="label">Logic Model Category</label>
                      <div class="control">
                        <div class="select">
                          <select v-model="form.type">
                            <option value="activity">Activity</option>
                            <option value="output">Output</option>
                            <option value="intermediate_outcome">
                              Intermediate Outcome
                            </option>
                            <option value="outcome">Outcome</option>
                            <option value="impact">Impact</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Column 2: Audience -->
                  <div class="column">
                    <div class="field">
                      <label class="label">SEM Level</label>
                      <div class="control">
                        <div class="select">
                          <select v-model="form.sem">
                            <option value="individual">Individual</option>
                            <option value="interpersonal">Interpersonal</option>
                            <option value="community">Community</option>
                            <option value="organizational">Organizational</option>
                            <option value="policy">Policy</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="column">
                    <div class="field">
                      <div class="control">
                        <label class="label">
                          Validated<br />
                          <input type="checkbox" v-model="form.is_validated" />
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!--
                  <div class="field">
                    <label class="label">Indicator</label>
                    <div class="control">
                      <input class="input" type="text" maxlength="80" v-model="selectedNode.indicator" />

                      <button class="button is-small" role="button"
                        @click.prevent="isIndicatorModalVisible = !isIndicatorModalVisible">
                        <span class="icon is-small mr-1">
                          <i class="fas fa-plus"></i>
                        </span>
                        Add Indicator
                      </button>
                    </div>
                  </div> -->


            <div class="field">
              <label class="label">Description</label>
              <div class="control">
                <textarea class="textarea" rows="4" columns="80" maxlength="999" v-model="form.description" />
              </div>
            </div>


            <!-- TODO: implement saving of indicators -->
            <div class="field">
              <label class="label">Indicators</label>

              <hr>

              <div class="field is-grouped is-grouped-multiline">
                <div class="control">
                  <div class="tags has-addons">
                    <a class="tag is-link">Technology</a>
                    <a class="tag is-delete"></a>
                  </div>
                </div>

                <div class="control">
                  <div class="tags has-addons">
                    <a class="tag is-link">CSS</a>
                    <a class="tag is-delete"></a>
                  </div>
                </div>

                <div class="control">
                  <div class="tags has-addons">
                    <a class="tag is-link">Flexbox</a>
                    <a class="tag is-delete"></a>
                  </div>
                </div>

                <div class="control">
                  <div class="tags has-addons">
                    <a class="tag is-link">Web Design</a>
                    <a class="tag is-delete"></a>
                  </div>
                </div>
              </div>

              <!-- <div class="control">
                      <input class="input" type="text" placeholder="Text input">
                    </div> -->
              <button class="button is-small" role="button"
                @click.prevent="isPanelVisible = !isPanelVisible; showIndicatorModal = true; useSideNavStore().hide();">
                <span class="icon is-small mr-1">
                  <i class="fas fa-plus"></i>
                </span>
                Add Indicator
              </button>
            </div>

          </form>
        </section>

        <footer class="modal-card-foot" style="display: block;">
          <div class="level">
            <div class="level-left">
              <div class="level-item">
                <button role="button" class="button is-small is-danger" @click="deleteItem()">
                  <span class="icon">
                    <i class="fas fa-trash"></i>
                  </span>
                  <!-- Delete Item -->
                </button>

              </div>
            </div>

            <div class="level-right">
              <div class="level-item">
                <button class="button is-primary" :class="{ 'is-loading': config.isLoading }" role="button"
                  @click.prevent="saveForm()">Save</button>
                <button class="button" role="button" @click="closeModal">Close</button>
              </div>
            </div>
          </div>
          <!-- <button class="button is-success">Save changes</button> -->
          <!-- <button class="button" @click="closeModal">Cancel</button> -->
        </footer>
      </div>

    </div>

  </div>
</template>

<style>
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
