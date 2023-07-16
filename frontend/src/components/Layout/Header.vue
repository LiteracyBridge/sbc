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
  MenuUnfoldOutlined,
  DownOutlined,
  AccountBookOutlined,
} from "@ant-design/icons-vue";
import {
  Popconfirm,
  Menu,
  DropdownButton,
  LayoutHeader,
  MenuItem,
  Space,
  Dropdown,
  Button,
  message,
  Divider,
} from "ant-design-vue";
import { useProjectStore } from "@/stores/projects";

const router = useRouter();
const userStore = useUserStore();
const sideNavStore = useSideNavStore();
const projectStore = useProjectStore();

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

function changeProject(prjId: number) {
  const project = projectStore.user_projects.find((prj) => prj.prj_id == prjId);

  message.success(`Switching active project to ${project?.name}`);

  projectStore.setPrj(prjId, false).then(() => window.location.reload());
  // router.push('/forms/basic');
}
</script>

<template>
  <LayoutHeader :has-sider="true" style="background: #ffffff; padding: 0px 16px 0px 0px">
    <div id="header-items">
      <span>
        <MenuUnfoldOutlined
          v-if="sideNavStore.visible"
          class="trigger"
          @click="() => (sideNavStore.visible = !sideNavStore.visible)" />
        <MenuUnfoldOutlined
          v-else
          class="trigger"
          @click="() => (sideNavStore.visible = !sideNavStore.visible)"
      /></span>

      <div>
        <Dropdown>
          <a @click.prevent style="color: inherit">
            {{ projectStore.projectName }}
            <DownOutlined />
          </a>

          <template #overlay>
            <Menu>
              <MenuItem v-for="prj in projectStore.projects()" :key="prj.prj_id">
                <Popconfirm
                  title="Are you sure to switch project?"
                  ok-text="Yes"
                  cancel-text="No"
                  @confirm="changeProject(prj.prj_id)"
                >
                  <a href="javascript:;">{{ prj.name }}</a>
                </Popconfirm>
              </MenuItem>
            </Menu>
          </template>
        </Dropdown>
      </div>

      <div>
        <Space style="padding-right: 52px">
          <span>Resources</span>
          <span>Help</span>
          <span>About</span>
        </Space>

        <Dropdown trigger="hover">
          <Button>
            {{ userStore.address_as }}

            <template #icon>
              <UserOutlined />
            </template>
          </Button>

          <template #overlay>
            <Menu>
              <MenuItem key="projects" :click="signOut">
                <RouterLink to="/projects">
                  <AppstoreOutlined />
                  <span> Manage Projects </span>
                </RouterLink>
              </MenuItem>

              <MenuItem key="profile" :click="signOut">
                <RouterLink to="/profile">
                  <UserOutlined />
                  <span> My Profile </span>
                </RouterLink>
              </MenuItem>

              <MenuItem key="logout" :click="signOut">
                <LogoutOutlined />
                <span> Logout </span>
              </MenuItem>
            </Menu>
          </template>
        </Dropdown>
      </div>
    </div>

    <!-- Place a dropdown at the end of the header -->

    <!-- <Header></Header> -->
  </LayoutHeader>
</template>

<style scoped>
#header-items {
  width: 100%;
  justify-content: space-between;
  display: inline-flex;
}
</style>
