<script lang="ts" setup>
import { onMounted, ref, reactive, watch } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router'
import { Button, TabPane, Table, Tabs, Tag, Typography } from "ant-design-vue";
import { PlusCircleOutlined } from "@ant-design/icons-vue";

import Activities from "./Activities.vue";


const config = ref({
  activeTab: 'activities'
})


</script>

<template>
  <section class="section">
    <Tabs v-model:activeKey="config.activeTab" centered class="my-3 mx-3">
      <TabPane key="activities" tab="Activities">
        <Activities></Activities>
      </TabPane>
    </Tabs>
  </section>
</template>

<style>
</style>
