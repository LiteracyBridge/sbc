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
  id: number = undefined;
  name: string = "";
  description: string = "";
  type_id: number = undefined;
  from_id?: number = undefined;
  to_id?: number = undefined;
  sem_id?: number;
  theory_of_change_id: number;
  is_validated: boolean = false;

  indicators: Array<{
    id: number;
    theory_of_change_id: number;
    indicator_id: number;
    indicator: IndicatorGroup;
  }> = [];
}

export class Risk {
  id: number = undefined;
  name: string = "";
  assumptions: string = "";
  mitigation: string = "";
  risks: string = "";

  project_id?: number = null;
  toc_from_id?: number = null;
  toc_to_id?: number = null;
  theory_of_change_id?: number = null;
}

export class TheoryOfChange {
  graph: Array<TheoryOfChangeItem> = [];
  id: string = null;
  risks: Risk[] = [];
  // indicators: any[] = [];
}
