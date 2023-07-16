<script setup lang="ts">
import { ref } from "vue";
import { Auth } from "aws-amplify";
import { useUserStore } from "@/stores/user";
import { useSideNavStore } from "@/stores/sideNav";
import { useRouter } from "vue-router";
import {
  AppstoreFilled,
  AppstoreOutlined,
  LogoutOutlined,
  UserOutlined,
  MenuUnfoldOutlined
} from "@ant-design/icons-vue";
import { Menu, DropdownButton, LayoutHeader, MenuItem, Space } from "ant-design-vue";

const router = useRouter();
const userStore = useUserStore();
const sideNavStore = useSideNavStore();

async function signOut() {
  try {
    await Auth.signOut().then((resp) => {
      userStore.setUser();
      sideNavStore.hide();

      router.push("/login");
      window.location.reload();
    });
  } catch (error) {
    userStore.setUser();
    router.push("/login");

    window.location.reload();
    console.log("error signing out: ", error);
  }
}
</script>

<template>
  <LayoutHeader :has-sider="true" style="background: #ffffff; padding: 0px 16px 0px 0px">
    <MenuUnfoldOutlined
      v-if="sideNavStore.visible"
      class="trigger"
      @click="() => (sideNavStore.visible = !sideNavStore.visible)"
    />
    <MenuUnfoldOutlined
      v-else
      class="trigger"
      @click="() => (sideNavStore.visible = !sideNavStore.visible)"
    />

    <div style="float: right">
      <Space style="padding-right: 52px">
        <span>Resources</span>
        <span>Help</span>
        <span>About</span>
      </Space>

      <DropdownButton trigger="hover">
        {{ userStore.address_as }}
        <template #overlay>
          <Menu>
            <MenuItem key="logout" :click="signOut">
              <RouterLink to="/projects">
                <span>
                  <AppstoreOutlined />
                  Project
                </span>
              </RouterLink>
            </MenuItem>

            <MenuItem key="logout" :click="signOut">
              <span>
                <LogoutOutlined />
                Logout
              </span>
            </MenuItem>
          </Menu>
        </template>

        <template #icon>
          <UserOutlined />
        </template>
      </DropdownButton>
    </div>
    <!-- Place a dropdown at the end of the header -->

    <!-- <Header></Header> -->
  </LayoutHeader>
</template>

<style></style>
