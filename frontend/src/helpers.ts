import dayjs from "dayjs";
import type { Dayjs } from "dayjs";

export const formatDate = (date?: string | Dayjs) => {
  if (date == null) return null;

  return dayjs(date).format("MMMM D, YYYY");
};

export const toBase64 = (file: any) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });
