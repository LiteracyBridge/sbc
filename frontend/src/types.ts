export interface IUser {
  id: number;
  email: string;
  name: string;
}

export interface IndicatorType {
  id: number;
  name: string;
  parent_id?: number;
}

export interface IndicatorGroup {
  id: number;
  name: string;
  group_id: number;
  // level: string;
  phrasing: string;
  purpose: string;
  link: string;
}

export class TheoryOfChangeItem {
  name: string = "";
  from_id?: number = undefined;
  to_id?: number = undefined;
  sem_id?: string;
  theory_of_change_id: number;
  indicators: any[] = [];
}

export class TheoryOfChange {
  graph: Array<TheoryOfChangeItem> = [];
  id: string = null;
  // indicators: any[] = [];
}
