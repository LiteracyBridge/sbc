<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import {
  Popconfirm,
  Checkbox,
  Button,
  Card,
  Col,
  Divider,
  Form,
  FormItem,
  Input,
  Modal,
  Popover,
  Row,
  Select,
  SelectOption,
  Space,
  Spin,
  Switch,
  Textarea,
  message,
  Empty,
  Tag,
  Tooltip,
} from "ant-design-vue";
import { ApiRequest } from "@/apis/api";
import { TheoryOfChange, THEORY_OF_CHANGE_TYPES, SEMS } from "@/types";

import IndicatorBrowserPanel from "./IndicatorBrowserPanel.vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { useProjectStore } from "@/stores/projects";
import { CloseOutlined, DeleteOutlined, PlusCircleOutlined } from "@ant-design/icons-vue";
import { useUserStore } from "@/stores/user";

const emit = defineEmits<{
  (e: "saved", data: TheoryOfChange[]): TheoryOfChange[];
  (e: "closed"): void;
  (e: "deleted", id: number): number;
}>();

const props = defineProps<{ visible: boolean; toc?: TheoryOfChange }>();

const store = useTheoryOfChangeStore(),
  projectStore = useProjectStore();

const config = ref({
  visible: props.visible,
  deleting: false,
  loading: false,
  form: props.toc || new TheoryOfChange(),
  browserVisible: false,
  new_indicators: [],
});

watch(props, (newProps) => {
  config.value.visible = newProps.visible;
  config.value.form = newProps.toc || new TheoryOfChange();
});

const isNew = computed(() => config.value.form?.id == null);

const getTocItemIndicators = computed(() => {
  if (isNew.value) return config.value.new_indicators || [];

  return store.getTocItemIndicators(config.value.form?.id) ?? [];
});

const closeModal = () => {
  config.value.visible = false;
  config.value.form = new TheoryOfChange();
  config.value.new_indicators = [];

  emit("closed");
};

function saveFormItem() {
  const fields = config.value.form;
  const data = {
    ...fields,
    is_validated: fields.is_validated || false,
    editing_user_id: useUserStore().id,
    new_indicators: config.value.new_indicators,
  };

  config.value.loading = store.isLoading;

  store
    .addTocItem(data)
    .then((resp) => {
      store.theory_of_change = resp;
      emit("saved", resp);
      closeModal();
    })
    .finally(() => (config.value.loading = store.isLoading));
}

function deleteItem() {
  config.value.deleting = true;

  ApiRequest.delete(`theory-of-change/${projectStore.prj_id}/item/${props.toc?.id}`)
    .then((_) => {
      emit("deleted", props.toc?.id);
      closeModal();
      message.success("Item deleted successfully");
    })
    .finally(() => {
      config.value.deleting = false;
    });
}

function indicatorSaved(resp: TheoryOfChange[]) {
  config.value.form = resp.find((i) => i.id == config.value.form.id);
}

function deleteIndicator(id: number) {
  store
    .saveIndicators({
      tocId: config.value.form.id,
      data: [{ id: id, is_deleted: true, name: "", is_new: false }],
    })
    .then((resp) => {
      indicatorSaved(resp);
      message.success("Indicator deleted successfully");
    });
}

const getTocList = computed(() => {
  if (config.value.form?.type_id == null) {
    return store.data;
  }
  return store.data.filter((item) => item.type_id > config.value.form?.type_id);
});
</script>

<template>
  <Modal
    v-model:open="config.visible"
    @cancel="closeModal()"
    @ok="closeModal()"
    width="700px"
  >
    <!-- IndiKit Browser Panel -->
    <IndicatorBrowserPanel
      :is-visible="config.browserVisible"
      @is-closed="config.browserVisible = false"
      :toc-item="config.form"
      @is-saved="indicatorSaved($event)"
      @save="config.new_indicators = $event"
    >
    </IndicatorBrowserPanel>

    <template #footer>
      <div style="width: 100%; display: flex; justify-content: space-between">
        <Popconfirm
          title="Are you sure? All its indicators and activities will be deleted!"
          ok-text="Yes"
          cancel-text="No"
          @confirm="deleteItem()"
        >
          <Button
            role="button"
            type="primary"
            :danger="true"
            v-if="!isNew"
            :loading="config.deleting"
            :disabled="config.deleting"
          >
            <DeleteOutlined />
            Delete
          </Button>
        </Popconfirm>

        <Space>
          <Button
            type="primary"
            :loading="config.loading"
            :disabled="config.loading"
            role="button"
            @click.prevent="saveFormItem()"
          >
            {{ isNew ? "Save" : "Update" }}
          </Button>

          <Button role="button" @click="closeModal()">Cancel</Button>
        </Space>
      </div>
    </template>

    <Spin :spinning="config.loading || config.deleting || store.isLoading">
      <Form layout="vertical" :model="config.form">
        <FormItem
          name="name"
          label="Label"
          has-feedback
          :rules="[{ required: true, message: 'Please enter theory of change label!' }]"
        >
          <Input v-model:value="config.form.name" placeholder="Enter label" />
        </FormItem>

        <Row :gutter="8">
          <Col :span="12">
            <FormItem label="Links To" name="links_to">
              <!-- TODO: show list of existing indicators -->
              <Select
                v-model:value="config.form.links_to"
                :allow-clear="true"
                mode="multiple"
              >
                <SelectOption v-for="item in getTocList" :key="item.id" :value="item.id">
                  {{ item.name }}
                </SelectOption>
              </Select>
            </FormItem>
          </Col>

          <Col :span="12">
            <FormItem
              name="type_id"
              label="Logic Model Category"
              has-feedback
              :rules="[{ required: true, message: 'Please select a category model!' }]"
            >
              <Select v-model:value="config.form.type_id">
                <SelectOption
                  v-for="key in Object.keys(THEORY_OF_CHANGE_TYPES)"
                  :key="key"
                  :value="+key"
                >
                  {{ THEORY_OF_CHANGE_TYPES[key] }}
                </SelectOption>
              </Select>
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="8">
          <Col :span="12">
            <FormItem name="sem_id" label="SEM Level">
              <Select v-model:value="config.form.sem_id" :allow-clear="true">
                <SelectOption v-for="key in Object.keys(SEMS)" :key="key" :value="+key">
                  {{ SEMS[key] }}
                </SelectOption>
              </Select>
            </FormItem>
          </Col>

          <Col :span="12">
            <FormItem
              name="is_validated"
              label="Is Theory of Change Validated?"
              has-feedback
              :rules="[{ required: false }]"
            >
              <Checkbox v-model:checked="config.form.is_validated">Validated</Checkbox>
            </FormItem>
          </Col>
        </Row>

        <!-- <div class="field">
            <div class="control">
              <label class="label">
                Validated
                <input type="checkbox" class="ml-3" v-model="tocItemModalConfig.form.is_validated" />
              </label>
            </div>
          </div> -->

        <FormItem
          name="description"
          label="Description"
          has-feedback
          :rules="[{ required: false }]"
          :show-count="false"
        >
          <Textarea v-model:value="config.form.description" :show-count="false">
          </Textarea>
        </FormItem>

        <!-- Indicators -->
        <!-- <div v-if="props.toc?.id != null"> -->
          <!-- <div class="field"> -->
          <Divider>Indicators</Divider>

          <!-- <Divider></Divider> -->
          <Empty
            description="No indicators added yet."
            v-if="getTocItemIndicators?.length == 0"
          >
          <!-- <template ></template> -->
          </Empty>

          <template v-else v-for="(item, index) in getTocItemIndicators" :key="item.id">
            <!-- TODO: open indicator browser on click -->
            <Tag
              :closable="true"
              @click="config.browserVisible = true"
              @close="deleteIndicator(item.id)"
            >
              {{ item.name }}
            </Tag>
          </template>

          <Button
            style="margin-top: 10px"
            size="small"
            role="button"
            @click="config.browserVisible = !config.browserVisible"
          >
            <PlusCircleOutlined />
            Add or Edit Indicators
          </Button>
        <!-- </div> -->
        <!-- </div> -->
      </Form>
    </Spin>
  </Modal>
</template>
