<script setup lang="ts">
import html2pdf from "html2pdf.js";

import {
  Avatar,
  Button,
  Card,
  Drawer,
  List,
  ListItem,
  ListItemMeta,
  Modal,
  Typography,
  message,
} from "ant-design-vue";
import ProjectSummary from "./ProjectSummary.vue";
import { onMounted, ref } from "vue";
import { Organisation } from "@/types";
import { ApiRequest } from "@/apis/api";
import { useUserStore } from "@/stores/user";
import { useProjectStore } from "@/stores/projects";
import { DownloadOutlined, FilePdfOutlined } from "@ant-design/icons-vue";

const config = ref({
  organisation: null as Organisation,
  showModal: false,
});

onMounted(() => {
  ApiRequest.get<Organisation>(`organisation/${useUserStore().id}`).then((data) => {
    config.value.organisation = data[0];
  });
});

function exportToPDF() {
  html2pdf(document.getElementById("summary-doc"), {
    margin: 1,
    filename: `${useProjectStore().projectName}-summary.pdf`,
  }).then((pdf) => {
    // pdf.save();
    config.value.showModal = false;
  })

  message.success("Project summary exported to PDF");
}
</script>

<template>
  <!-- <Card title="Project Documents" :bordered="false"> -->
  <List size="small" item-layout="horizontal" bordered>
    <template #header>
      <Typography.Title :level="5">Project Documents</Typography.Title>
    </template>

    <ListItem>
      <ListItemMeta>
        <template #avatar>
          <Avatar>
            <template #icon>
              <FilePdfOutlined />
            </template>
          </Avatar>
        </template>

        <template #title>
          <a href="#" @click.prevent="config.showModal = true">Project summary</a>
        </template>

        <template #description>
          <span>Download project summary as a PDF</span>
        </template>
      </ListItemMeta>
    </ListItem>
  </List>

  <Drawer
    v-model:open="config.showModal"
    width="80vw"
    title="Download project summary document"
    @cancel="config.showModal = false"
    @hide-okay="true"
  >
    <template #extra>
      <Button type="primary" :ghost="true" @click="exportToPDF()">
        <DownloadOutlined /> Download
      </Button>
    </template>

    <div
      id="summary-doc"
      style="margin: 2cm 2cm 2.5cm 2cm"
      v-if="config.organisation != null"
    >
      <ProjectSummary :organisation="config.organisation"></ProjectSummary>
    </div>
  </Drawer>
  <!-- </Card> -->
</template>
