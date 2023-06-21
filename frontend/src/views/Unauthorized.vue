<script setup lang="ts">
import { ApiRequest } from '@/apis/api';
import { Button, Card, Result, FormItem, Form, Input, Textarea, Row, Col, Space, TypographyParagraph, type FormInstance, message, Modal } from 'ant-design-vue';
import { h, ref } from 'vue';


const config = ref({
  form: {
    notes: null,
    name: null,
    email: null
  },
  loading: false
});
const accessForm = ref<FormInstance>();

function save() {
  accessForm.value.validate().then(() => {
    config.value.loading = true;

    ApiRequest.post("organisation/access-request", config.value.form)
      .then((_) => {
        // message.success("Access request sent successfully");

        Modal.success({
          title: 'Access Request Received',
          content: h('p', 'Thank you for your interest in the SBC Platform. We have received your request and will get back to you as soon as possible.'),
        });
      })
      .finally(() => {
        config.value.loading = false;
      });
  });
}
</script>

<template>
  <!-- Create a contact form for users to request access to the system -->
  <!-- <Row>
    <Col :span="8">
    </Col>
    <Col :span="8"> -->
  <Space direction="horizontal" style="width: 100%; justify-content: center">
    <Card title="Request Access" class="" style="width: 40em;">
      <TypographyParagraph>
        If you would like to request access to the system, please fill out the form below and we will get back to you as
        soon as possible. <br>

        For additional information, email us on <a href="mailto:support@amplio.org">support@amplio.org</a>

        <br><br>
      </TypographyParagraph>

      <Form layout="vertical" ref="accessForm" name="access-form" :model="config.form">
        <FormItem label="Organisation Name" name="name" has-feedback
          :rules="[{ required: true, message: 'Please enter organisation name!' }]">
          <Input type="text" v-model:value="config.form.name" />
        </FormItem>

        <FormItem label="Email" name="email" has-feedback
          :rules="[{ email: true, required: true, message: 'Please enter a valid email!' }]">
          <Input type="email" v-model:value="config.form.email" />
        </FormItem>

        <FormItem label="Tell us about what you do and your use case of the SBC Platform" name="notes" has-feedback
          :rules="[{ required: true, message: 'Please tell us about your organisation and why you think we can help you' }]">

          <Textarea :rows="10" v-model:value="config.form.notes"></Textarea>
        </FormItem>


        <Button type="primary" @click="save()" :loading="config.loading">Request Access</Button>
      </Form>
    </Card>
  </Space>

  <!-- </Col>
    <Col :span="8">
    </Col>
  </Row> -->

  <!-- <Result status="403" title="403" sub-title="Sorry, you are not authorized to access this page.">
    <template #extra>
      <RouterLink to="/login">
        <Button type="primary">Back Home</Button>
      </RouterLink>
    </template>
  </Result> -->
</template>

<style>
.center {
  min-height: 10em;
  display: table-cell;
  vertical-align: middle
}
</style>
