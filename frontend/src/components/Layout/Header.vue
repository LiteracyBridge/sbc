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
  Tooltip,
} from "ant-design-vue";
import { useProjectStore } from "@/stores/projects";
import Profile from "@/views/Profile.vue";
import FeedbackModal from "@/components/FeedbackModal.vue";

const router = useRouter();
const userStore = useUserStore();
const sideNavStore = useSideNavStore();
const projectStore = useProjectStore();

const profileVisible = ref(false),
  feedbackModalVisible = ref(false);

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
  <Profile :visible="profileVisible" @close="profileVisible = false"></Profile>

  <FeedbackModal :visible="feedbackModalVisible" @close="feedbackModalVisible = false">
  </FeedbackModal>

  <LayoutHeader
    :has-sider="true"
    style="background: #289b6a; padding: 0px 16px 0px 0px; color: white"
  >
    <div id="header-items">
      <div>
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

        <Dropdown :trigger="['click']">
          <Tooltip title="Click to change project">
            <a @click.prevent style="color: inherit">
              {{ projectStore.projectName }}
              <DownOutlined />
            </a>
          </Tooltip>

          <template #overlay>
            <Menu>
              <MenuItem v-for="prj in projectStore.projects()" :key="prj.id">
                <Popconfirm
                  title="Are you sure to switch project?"
                  ok-text="Yes"
                  cancel-text="No"
                  @confirm="changeProject(prj.id)"
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

          <!-- <span>Help</span> -->
          <span>About</span>

          <Divider type="vertical" style="background-color: white" />

          <Dropdown>
            <span>
              Need Help?
              <DownOutlined />
            </span>

            <template #overlay>
              <Menu>
                <MenuItem>
                  <a href="#" @click.prevent="feedbackModalVisible = true"
                    >Sends Us Feedback</a
                  >
                </MenuItem>

                <MenuItem>
                  <Tooltip
                    title="You will be taken to a Discourse, a discussion forum for the Impact Designer"
                  >
                    <a href="https://sbcimpact.discourse.group" target="_blank" rel="noopener"
                      >Join Discussion</a
                    >
                  </Tooltip>
                </MenuItem>
              </Menu>
            </template>
          </Dropdown>

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
              <MenuItem key="projects">
                <RouterLink to="/projects">
                  <AppstoreOutlined />
                  <span> Manage Projects </span>
                </RouterLink>
              </MenuItem>

              <MenuItem key="profile" @click="profileVisible = true">
                <UserOutlined />
                <span> My Profile </span>
              </MenuItem>

              <MenuItem key="logout" @click="signOut">
                <LogoutOutlined />
                <span> Logout </span>
              </MenuItem>
            </Menu>
          </template>
        </Dropdown>
      </div>
    </div>

  </LayoutHeader>
</template>

<style scoped>
#header-items {
  width: 100%;
  justify-content: space-between;
  display: inline-flex;
}
</style>
