<script setup lang="ts">

import { Card, Form, FormItem, Select, SelectOption, Textarea, type FormInstance, Row, Col } from 'ant-design-vue';
import { ref, watch } from 'vue';
import { useProjectDataStore } from '@/stores/projectData';
import GPTSuggestionPanel from '@/components/GPTSuggestionPanel.vue';
import { useTheoryOfChangeStore } from '@/stores/theory_of_change'
import BroadcastComponent from '@/components/BroadcastComponent.vue';


const BULB_ICON = "/images/lightbulb.png"

const projectDataStore = useProjectDataStore();

const config = ref({
  messages: false,
  loading: false,
  suggestions: {
    questionId: null,
    isOpened: false,
    module: "basic"
  },
});

function showPanel(id: string | number) {
  config.value.suggestions.questionId = id;
  config.value.suggestions.module = config.value.suggestions.module;
  config.value.suggestions.isOpened = true;
}

function updateData(event: any, id: number) {
  projectDataStore.setData(id, event.target.value);
}

const updateSector = (value: any, id: number) => {
  projectDataStore.setData(id, value);
}
</script>

<template>
  <GPTSuggestionPanel
    :is-visible="config.suggestions.isOpened"
    @is-closed="config.suggestions.isOpened = false"
    :question-id="config.suggestions.questionId"
    :module="config.suggestions.module"
  >
  </GPTSuggestionPanel>

  <Card title="Project Info" :loading="config.loading">
    <BroadcastComponent :module="config.suggestions.module"></BroadcastComponent>

    <Form layout="vertical">
      <Row>
        <Col :span="14">
          <FormItem
            :name="`input-${count + 1}`"
            v-for="(q, count) in projectDataStore.questionsForTopic(
              config.suggestions.module
            )"
            :key="q.id"
          >
            <template #label> {{ count + 1 }}. {{ q.q2u }} </template>
            <!-- <label class="label" :for="`input-${count + 1}`">{{ count + 1 }}. {{ q.q2u }}</label> -->

            <!-- Use dropdown for sectors -->
            <Select
              v-if="q.id == 1"
              :value="projectDataStore.getData(q.id)"
              @change="updateSector($event, q.id)"
              style="padding-bottom: 15px"
            >
              <SelectOption
                v-for="(sector, index) in useTheoryOfChangeStore().getIndiKitSectors"
                :key="index"
                :value="sector"
              >
                {{ sector }}
              </SelectOption>
            </Select>

            <!-- <div class="control"> -->
            <img
              v-if="q.bulb"
              :src="BULB_ICON"
              ref="iconRefs"
              @click="showPanel(q.id)"
              class="image is-32x32"
            />

            <Textarea
              v-if="q.id != 1"
              @change="updateData($event, q.id)"
              :value="projectDataStore.getData(q.id)"
              :rows="7"
              :cols="40"
            ></Textarea>
          </FormItem>
        </Col>
      </Row>
    </Form>
  </Card>
</template>
