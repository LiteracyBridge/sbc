import { defineStore } from "pinia";
import { useProjectStore } from "./projects";
import axios from "axios";
import { SBC_TW_URL } from "../apis/lambda";

export const useMessageStore = defineStore({
  id: "messages",
  state: () => ({
    lastSentId: 0,
    lastReceivedId: 0,
    messages: {},
  }),
  getters: {
    messagesForTopic: (state) => (topic) =>
      state.messages[topic] ? state.messages[topic] : {},
  },
  actions: {
    // Fetches the latest messages for the specified related_item and updates the store state
    async getLatestMessages(related_item, messages) {
      const queryString =
        "?prj_id=" +
        useProjectStore().prj_id +
        "&related_item=" +
        related_item +
        "&since_sent_id=" +
        this.lastSentId +
        "&since_received_id=" +
        this.lastReceivedId;
      let topicMsgs = [];
      topicMsgs = this.messagesForTopic(related_item);

      if (related_item in messages) {
        topicMsgs = messages[related_item];
      } else {
        topicMsgs = messages[related_item] = {};
      }

      const response = await axios.get(SBC_TW_URL + queryString);
      const rows = response.data;
      for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const s_id = row[0];
        const s_time = row[1];
        const s_uid = row[2];
        const s_msg = row[3];
        const r_id = row[4];
        const r_time = row[5];
        const r_uid = row[6];
        const r_msg = row[7];

        // if (s_id) {
        //   this.lastSentId = s_id;
        // }
        // if (r_id) {
        //   this.lastReceivedId = r_id;
        // }

        if (!(s_id in messages[related_item])) {
          // new sent message
          topicMsgs[s_id] = {
            time: s_time,
            user_id: s_uid,
            message: s_msg,
            replies: {},
          };
        }
        if (r_id !== null && r_msg != "Yes - Send Update") {
          topicMsgs[s_id].replies[r_id] = {
            time: r_time,
            user_id: r_uid,
            message: r_msg,
          };
        }
      }

      return topicMsgs;
    },
  },
});
