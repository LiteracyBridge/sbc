<script setup lang="ts">
import { Card, Row, Col, Avatar, Typography, Space, Image, Divider } from 'ant-design-vue';

</script>

<template>
  <Card title="Partners" class="section" :bordered="false">
    <p style="font-style: italic; margin-bottom: 40px;">
      <!-- Write a brief intro about the project partners -->
      The project would not be possible without the help of our partners. They provided resources and the expertise to
      make this project a reality.
      <!-- <Divider  :dashed="true"></Divider> -->
    </p>


    <Row :gutter="2">

      <Col :span="4">
      <div class="partner-image">
        <Image src="https://fastly.picsum.photos/id/76/200/300.jpg?hmac=SWpe2KMM2qFiQ8C8WHIZilaJb7KVkgOVVJPTbasGyUU">
        </Image>

        <Typography.Title :level="5"> Partner 1</Typography.Title>
      </div>
      </Col>

      <Col :span="18">
      <Typography.Paragraph>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Atque sapiente optio non ex beatae
        nostrum quasi animi
        maiores! Doloribus incidunt officia aliquid adipisci quaerat id porro corporis neque rerum quis. <br>

        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dignissimos commodi corrupti, tenetur assumenda vel
        laborum quibusdam illo quod ratione inventore vero, pariatur eum non ea amet maiores consectetur. Voluptatibus,
        voluptate!
      </Typography.Paragraph>
      </Col>
    </Row>


    <Row :gutter="2" style="margin-top: 15px;">

      <Col :span="4">
      <div class="partner-image">
        <Image src="https://fastly.picsum.photos/id/76/200/300.jpg?hmac=SWpe2KMM2qFiQ8C8WHIZilaJb7KVkgOVVJPTbasGyUU">
        </Image>

        <Typography.Title :level="5"> Partner 2</Typography.Title>
      </div>
      </Col>

      <Col :span="18">
      <Typography.Paragraph>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Atque sapiente optio non ex beatae
        nostrum quasi animi
        maiores! Doloribus incidunt officia aliquid adipisci quaerat id porro corporis neque rerum quis. <br>

        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dignissimos commodi corrupti, tenetur assumenda vel
        laborum quibusdam illo quod ratione inventore vero, pariatur eum non ea amet maiores consectetur. Voluptatibus,
        voluptate!
      </Typography.Paragraph>
      </Col>
    </Row>

  </Card>
</template>

<style>
.partner-image {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 40%;
}

.partner-image>.ant-typography {
  margin-top: 10px;
}
</style>
