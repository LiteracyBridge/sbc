<script setup lang="ts">
import html2pdf from "html2pdf.js";
import { Card, List, ListItem, Typography } from "ant-design-vue";

import ProjectSummary from "./ProjectSummary.vue";

function exportToPDF() {
  html2pdf(document.getElementById("element-to-convert"), {
    margin: 1,
    filename: "i-was-html.pdf",
  });
}
</script>

<template>
  <div id="element-to-convert" style="margin: 2cm 2cm 2.5cm 2cm">
    <ProjectSummary></ProjectSummary>
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
