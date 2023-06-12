<script setup lang="ts">

import { Card, Form, FormItem, Image, Textarea } from 'ant-design-vue';
import { ref } from 'vue';

import { useProjectDataStore } from '@/stores/projectData';
import GPTSuggestionPanel from '@/components/GPTSuggestionPanel.vue';

const BULB_ICON = "/images/lightbulb.png"

const projectDataStore = useProjectDataStore();

const config = ref({
    suggestions: {
        questionId: null,
        isOpened: false,
        module: "objectives"
    }
});

function showPanel(id: string | number) {
    config.value.suggestions.questionId = id;
    config.value.suggestions.module = config.value.suggestions.module;
    config.value.suggestions.isOpened = true;
}

function updateData(event: any, id: number) {
    projectDataStore.setData(id, event.target.value);
}

</script>

<template>
    <GPTSuggestionPanel :is-visible="config.suggestions.isOpened" @is-closed="config.suggestions.isOpened = false;"
        :question-id="config.suggestions.questionId" :module="config.suggestions.module">
    </GPTSuggestionPanel>

    <Card class="section" title="Project Objectives">

        <Form layout="vertical">
            <!-- <div class="columns mx-4 is-vcentered"> -->

            <!-- <div class="column is-8"> -->

            <!-- <strong>{{ count + 1 }}. {{ q.q2u }} </strong><br />
  <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id, topic)"
    class="image is-32x32" />
  <textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" rows="4" cols="80" /><br />
  <br /><br /> -->

            <FormItem :name="`input-${count + 1}`"
                v-for="(q, count) in projectDataStore.questionsForTopic(config.suggestions.module)" :key="q.id">
                <template #label>
                    {{ count + 1 }}. {{ q.q2u }}
                </template>
                <!-- <label class="label" :for="`input-${count + 1}`">{{ count + 1 }}. {{ q.q2u }}</label> -->

                <!-- <div class="control"> -->
                <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="showPanel(q.id)" class="image is-32x32" />
                <!-- </div> -->

                <!-- <div class="control"> -->
                <Textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" :rows="7"
                    :cols="40" style="width: 70%;"></Textarea>

                <!-- </div> -->

            </FormItem>
            <!-- </div> -->

            <!-- </div> -->
        </Form>
    </Card>
</template>
