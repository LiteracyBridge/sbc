import { defineStore } from "pinia";
import { useProjectStore } from "./projects";
import axios from "axios";
import { useUserStore } from "./user";
import { ApiRequest } from "@/apis/api";

export const useOpenAIStore = defineStore({
  id: "open-ai-store",

  state: () => ({
    loading: false as boolean,
  }),

  actions: {
    async trackUsage(
      id: string | number,
      status: "accepted" | "rejected" | "error"
    ) {
      return ApiRequest.post("open-ai/usage", {
        id,
        status: status,
      });
    },
    countWords(str: string) {
      // Use a regular expression to match words, including words with apostrophes and hyphens
      const words = str.match(/\b[\w'-]+\b/g);

      // Return the number of words
      return words ? words.length : 0;
    },
    async gptCompletion(
      prompt: string,
      context: string = null,
      format: string = null,
      start: string = null,
      stop: string = null
    ) {
      this.$state.loading = true;

      // format can be "item","list","sentence", or "paragraph"
      // const payload = { prj_id, prompt, format, stop, start, context };

      // if (format) payload.format = format;
      // if (start) payload.start = start;
      // if (stop) payload.stop = stop;
      if (context) {
        console.log(
          "Words in GPT context + prompt: ",
          this.countWords(prompt) + this.countWords(context)
        );
        // payload.context = context;
      }

      // set to false when testing other features to avoid unnecessary calls to openai
      return ApiRequest.post<{ id: number; error?: string; result?: string }>(
        `open-ai`,
        {
          prompt: prompt,
          context: context,
          format: format,
          start: start,
          stop: stop,
          prj_id: useProjectStore().prj_id,
          user_id: useUserStore().id,
        }
      )
        .then(([resp]) => {
          const message = resp.result as string;
          return {
            id: resp.id,
            result: message,
            error:
              message.indexOf("Request failed after") > -1 ? message : null,
          };
        })
        .catch((error) => {
          console.log(error);
          this.$state.loading = false;
          return { error: error.message, id: null };
        })
        .finally(() => (this.$state.loading = false));
    },
  },
});
