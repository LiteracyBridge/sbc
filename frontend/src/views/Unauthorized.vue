<script setup lang="ts">
import { Button, Card, Result, FormItem, Form, Input, Textarea, Row, Col, Space, TypographyParagraph } from 'ant-design-vue';
import { ref } from 'vue';


const config = ref({
  form: {
    organisation: null,
  }
})
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
      <!-- <p>
        You can also contact us on <a href="mailto:support@amplio.org">support@amplio.org</a>
      </p> -->

      <Form layout="vertical">
        <FormItem label="Organisation Name" name="name" has-feedback
          :rules="[{ required: true, message: 'Please enter organisation name!' }]">
          <Input type="text" />
        </FormItem>

        <FormItem label="Email" name="email" has-feedback
          :rules="[{ required: true, message: 'Please enter a valid email!' }]">
          <Input type="email" />
        </FormItem>

        <FormItem label="Tell us about what you do and your use case of the SBC Platform" name="description" has-feedback
          :rules="[{ required: true, message: 'Please tell us about your organisation and why you think we can help you' }]">

          <Textarea :rows="10"></Textarea>
        </FormItem>


        <Button type="primary">Request Access</Button>
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
