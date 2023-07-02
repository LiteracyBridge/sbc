<script setup lang="ts">
import { ref } from 'vue'
import { Auth } from 'aws-amplify';
import { useUserStore } from '@/stores/user'
import { useSideNavStore } from "@/stores/sideNav";
import { useRouter } from 'vue-router';
import { AppstoreFilled, AppstoreOutlined, LogoutOutlined, UserOutlined } from '@ant-design/icons-vue';
import { Menu, DropdownButton, MenuItem, Space } from 'ant-design-vue';

const router = useRouter();
const userStore = useUserStore();
const sideNavStore = useSideNavStore();

async function signOut() {
  try {
    await Auth.signOut()
      .then((resp) => {
        userStore.setUser();
        sideNavStore.hide()

        router.push('/login');
        window.location.reload()
      })
  } catch (error) {
    userStore.setUser();
    router.push('/login')

    window.location.reload()
    console.log('error signing out: ', error);
  }
}

</script>

<template>
  <div style="float: right;">
    <Space style="padding-right: 52px;">
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
</template>

<style>
</style>
