import dayjs from "dayjs";
import type { Dayjs } from "dayjs";

export const formatDate = (date?: string | Dayjs) => {
  if (date == null) return null;

  return dayjs(date).format("MMMM D, YYYY");
};
