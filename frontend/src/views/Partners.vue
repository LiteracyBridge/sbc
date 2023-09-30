<script setup lang="ts">
import {
  Card,
  Row,
  Col,
  Avatar,
  Typography,
  Space,
  Image,
  Divider,
} from "ant-design-vue";
</script>

<template>
  <Card :bordered="false">
    <!-- <Typography.Title :level="3">About SBC Impact Designer</Typography.Title>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Id inventore officia optio cupiditate velit voluptas
      quidem mollitia exercitationem iste dignissimos laudantium animi quaerat eos et, expedita maxime vitae tenetur
      corporis.</p>

    <Divider></Divider> -->
    <Typography.Title :level="3">Funders &amp; Partners</Typography.Title>

    <p style="margin-bottom: 40px">
      <Typography.Paragraph>
        Amplio acknowledges our funding partners who have graciously supported the
        development of this software.</Typography.Paragraph
      >

      <!-- <Divider  :dashed="true"></Divider> -->
    </p>

    <Row>
      <Col :span="12">
        <Image src="/images/bmgf_logo.png" width="375px" height="170px"> </Image>
      </Col>
      <Col :span="12">
        <Image src="/images/arm_logo.png" class="mt-5 pt-5"> </Image>
      </Col>
    </Row>

    <p style="margin-bottom: 40px; margin-top: 60px">
      <Typography.Paragraph
        >Amplio also acknowledges our partners who have worked with us on the development
        of this software.</Typography.Paragraph
      >
    </p>
    <Row>
      <Col :span="12">
        <Image src="/images/people_in_need_logo.png" width="375px" height="170px">
        </Image>
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

.partner-image > .ant-typography {
  margin-top: 10px;
}
</style>
