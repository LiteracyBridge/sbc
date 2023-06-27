<script setup>
import { Authenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";
import LogoLarge from "@/assets/logo-large.png";
import { LayoutHeader, LayoutContent, Layout, LayoutFooter } from "ant-design-vue";

const formFields = {
  signIn: {
    username: {
      placeholder: 'Enter your email',
    },
  },
  signUp: {
    confirm_password: {
      label: 'Confirm Password:',
      order: 1,
    },
    password: {
      label: 'Password:',
      placeholder: 'Enter your Password:',
      isRequired: false,
      order: 2,
    },
  },
  forceNewPassword: {
    password: {
      placeholder: 'Enter your Password:',
    },
  },
  resetPassword: {
    username: {
      placeholder: 'Enter your email:',
    },
  },
  confirmResetPassword: {
    confirmation_code: {
      placeholder: 'Enter your Confirmation Code:',
      label: 'New Label',
      isRequired: false,
    },
    confirm_password: {
      placeholder: 'Enter your Password Please:',
    },
  },
  setupTOTP: {
    QR: {
      totpIssuer: 'test issuer',
      totpUsername: 'amplify_qr_test_user',
    },
    confirmation_code: {
      label: 'New Label',
      placeholder: 'Enter your Confirmation Code:',
      isRequired: false,
    },
  },
  confirmSignIn: {
    confirmation_code: {
      label: 'New Label',
      placeholder: 'Enter your Confirmation Code:',
      isRequired: false,
    },
  },
};
</script>

<template>
  <!-- Display the AWS Amplify Authenticator component -->
  <main>
    <!-- <LayoutHeader>Header</LayoutHeader> -->

    <!-- <LayoutContent> -->
    <authenticator :form-fields="formFields">
      <template v-slot:header>
        <div style="padding: var(--amplify-space-large); text-align: center">
          <img class="amplify-image" alt="Amplify logo" :src="LogoLarge" />
        </div>
      </template>

      <!-- <template v-slot:sign-in-header>
        <h3 class="amplify-heading" style="padding: var(--amplify-space-xl) 0 0 var(--amplify-space-xl)">
          SBC Impact Designer Login
        </h3>
      </template> -->

      <!-- <template v-slot:sign-in-footer>
      <div style="text-align: center">
        <a role="button" type="link" @click="toResetPassword">
          Reset Password
        </a>
      </div>
    </template> -->

    </authenticator>


    <!-- </LayoutContent> -->
    <!-- <footer>Footer</footer> -->
  </main>
</template>

<style>
.amplify-button[data-variation='primary'] {
  background-color: #48c78e;
}
</style>
