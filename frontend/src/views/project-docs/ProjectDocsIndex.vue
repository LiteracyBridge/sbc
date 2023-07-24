<script setup lang="ts">
import html2pdf from "html2pdf.js";
import { Card, List, ListItem, Typography } from "ant-design-vue";

import ProjectSummary from "./ProjectSummary.vue";
import { onMounted, ref } from "vue";
import { Organisation } from "@/types";
import { ApiRequest } from "@/apis/api";
import { useUserStore } from "@/stores/user";

const config = ref({
  organisation: null as Organisation,
});

onMounted(() => {
  ApiRequest.get<Organisation>(`organisation/${useUserStore().id}`).then((data) => {
    config.value.organisation = data[0];
  });
});

function exportToPDF() {
  html2pdf(document.getElementById("element-to-convert"), {
    margin: 1,
    filename: "i-was-html.pdf",
  });
}
</script>

<template>
  <div
    id="element-to-convert"
    style="margin: 2cm 2cm 2.5cm 2cm"
    v-if="config.organisation != null"
  >
    <ProjectSummary :organisation="config.organisation"></ProjectSummary>
  </div>

  <!-- <Card title="Project Documents" :bordered="false"> -->
  <List size="large" bordered>
    <template #header>
      <Typography.Title :level="5">Project Documents</Typography.Title>
    </template>

    <template #footer>
      <div>Footer</div>
    </template>

    <ListItem @click="exportToPDF()">Project summary</ListItem>
  </List>
  <!-- </Card> -->
</template>
