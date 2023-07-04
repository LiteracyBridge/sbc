<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import {
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
import { DeleteOutlined, PlusCircleOutlined } from "@ant-design/icons-vue";

const isPanelVisible = ref(false);
const showIndicatorModal = ref(false);

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
});

watch(props, (newProps) => {
  config.value.visible = newProps.visible;
  config.value.form = newProps.toc || new TheoryOfChange();
});

const isNew = computed(() => config.value.form?.id == null);

const getTocItemIndicators = computed(() => {
  if (isNew.value) return [];

  return store.theoryOfChangeItemIndicators(config.value.form?.id) ?? [];
});

const closeModal = () => {
  config.value.visible = false;
  config.value.form = new TheoryOfChange();

  emit("closed");
};

function saveFormItem() {
  const fields = config.value.form;
  const data = {
    name: fields.name,
    type_id: fields.type_id,
    from_id: fields.from_id,
    to_id: fields.to_id,
    sem_id: fields.sem_id,
    description: fields.description,
    is_validated: fields.is_validated || false,
  };

  config.value.loading = true;
  if (!isNew.value) {
    // Update item
    ApiRequest.put<TheoryOfChange>(
      `theory-of-change/${projectStore.prj_id}/item/${props.toc?.id}`,
      data
    )
      .then((resp) => {
        emit("saved", resp);
        closeModal();
        message.success("Item updated successfully");
      })
      .finally(() => {
        config.value.loading = false;
      });
  } else {
    //  Create item
    ApiRequest.post<TheoryOfChange>(`theory-of-change/${projectStore.prj_id}/item`, data)
      .then((resp) => {
        emit("saved", resp);
        closeModal();
        message.success("Item created successfully");
      })
      .finally(() => {
        config.value.loading = false;
      });
  }
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
      data: { removed: [id], removed_custom: [], added: [] },
    })
    .then((resp) => {
      indicatorSaved(resp);
      message.success("Indicator deleted successfully");
    });
}
</script>

<template>
  <Modal v-model:visible="config.visible" @ok="closeModal()">
    <!-- IndiKit Browser Panel -->
    <IndicatorBrowserPanel
      :is-visible="isPanelVisible"
      @is-closed="
        isPanelVisible = false;
        showIndicatorModal = true;
      "
      :toc-item="config.form"
      @is-saved="indicatorSaved($event)"
    >
    </IndicatorBrowserPanel>

    <template #footer>
      <footer style="display: block">
        <div class="level">
          <div class="level-left">
            <div class="level-item">
              <Button
                role="button"
                type="primary"
                :danger="true"
                @click="deleteItem()"
                v-if="!isNew"
                :class="{ 'is-loading disabled': config.deleting }"
                :disabled="config.deleting"
              >
                <DeleteOutlined />
                Delete
              </Button>
            </div>
          </div>

          <div class="level-right">
            <div class="level-item">
              <Button
                type="primary"
                :class="{ 'is-loading': config.loading }"
                :disabled="config.loading"
                role="button"
                @click.prevent="saveFormItem()"
              >
                {{ isNew ? "Save" : "Update" }}
              </Button>

              <Button role="button" @click="closeModal()">Cancel</Button>
            </div>
          </div>
        </div>
      </footer>
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

        <Row :gutter="4">
          <Col :span="12">
            <FormItem label="Links From" name="from_id">
              <!-- TODO: show list of existing indicators -->
              <Select v-model:value="config.form.from_id" :allow-clear="true">
                <SelectOption v-for="item in store?.data" :key="item.id" :value="item.id">
                  {{ item.name }}
                </SelectOption>
              </Select>
            </FormItem>
          </Col>

          <Col :span="12">
            <FormItem label="Links To" name="to_id">
              <!-- TODO: show list of existing indicators -->
              <Select v-model:value="config.form.to_id" :allow-clear="true">
                <SelectOption v-for="item in store?.data" :key="item.id" :value="item.id">
                  {{ item.name }}
                </SelectOption>
              </Select>
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="4">
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

          <Col :span="12">
            <FormItem name="sem_id" label="SEM Level">
              <Select v-model:value="config.form.sem_id" :allow-clear="true">
                <SelectOption v-for="key in Object.keys(SEMS)" :key="key" :value="+key">
                  {{ SEMS[key] }}
                </SelectOption>
              </Select>
            </FormItem>
          </Col>
        </Row>

        <FormItem
          name="is_validated"
          label=""
          has-feedback
          :rules="[{ required: false }]"
        >
          <Checkbox v-model:checked="config.form.is_validated">Validated</Checkbox>
        </FormItem>

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
        >
          <Textarea v-model:value="config.form.description"> </Textarea>
        </FormItem>

        <!-- Indicators -->
        <div v-if="props.toc?.id != null">
          <!-- <div class="field"> -->
          <Divider>Indicators</Divider>

          <!-- <Divider></Divider> -->
          <Empty
            description="No indicators added yet."
            v-if="getTocItemIndicators?.length == 0"
          ></Empty>

          <template
            v-else
            v-for="(item, index) in store.theoryOfChangeItemIndicators(config.form.id)"
            :key="item.id"
          >
            <Tooltip :title="item.name">
              <Tag :closable="true" @close="deleteIndicator(item.id)">
                {{ item.name }}
              </Tag>
            </Tooltip>
          </template>

          <Button
            size="small"
            role="button"
            @click="
              isPanelVisible = !isPanelVisible;
              showIndicatorModal = true;
            "
          >
            <PlusCircleOutlined />
            Add Indicator
          </Button>
        </div>
        <!-- </div> -->
      </Form>
    </Spin>
  </Modal>
</template>

<style></style>
