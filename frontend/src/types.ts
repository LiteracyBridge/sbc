interface IUser {
  id: number;
  email: string;
  name: string;
}

interface IndicatorType {
  id: number;
  name: string;
  parent_id?: number;
}

interface IndicatorGroup {
    id: number;
    name: string;
    group_id: number;
    // level: string;
    phrasing: string;
    purpose: string;
    link: string;
}
