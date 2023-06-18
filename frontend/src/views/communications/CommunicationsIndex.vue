<script setup lang="ts">
import { Card, CollapsePanel, Collapse, Descriptions, DescriptionsItem } from 'ant-design-vue';
import { ref } from 'vue';

const config = ref({
    loading: false,
    collapseKey: ''
})

</script>

<template>
    <Card title="Communications and Messaging">
        <Collapse v-model:activeKey="config.collapseKey">
            <CollapsePanel key="1" header="This is panel header 1">

                <Descriptions :column="2" bordered>
                    <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Product">Cloud Database
                    </DescriptionsItem>
                    <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Product">Cloud Database
                    </DescriptionsItem>
                    <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Product">Cloud Database
                    </DescriptionsItem>
                </Descriptions>

            </CollapsePanel>
        </Collapse>

    </Card>
</template>
