<script setup lang="ts">
import { Button, Result } from 'ant-design-vue';

</script>

<template>
    <Result status="403" title="403" sub-title="Sorry, you are not authorized to access this page.">
        <template #extra>
            <RouterLink to="/login">
                <Button type="primary">Back Home</Button>
            </RouterLink>
        </template>
    </Result>
</template>
