export class User {
  id: number;
  email: string;
  name: string;
  address_as?: string;
  token?: string;
  last_project_id?: number;
  organisation_id?: number;
}

export class IndicatorType {
  id: number;
  name: string = '';
  parent_id?: number;
}

export class IndicatorGroup {
  id: number;
  name: string = "";
  group_id: number;
  // level: string;
  phrasing: string = "";
  purpose: string = "";
  link: string = "";
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

  indicators: Array<TheoryOfChangeIndicator> = [];
}

class TheoryOfChangeIndicator {
  id: number;
  toc_item_id: number;
  indicator_id: number;
  indicator: IndicatorGroup;

  toc_item: TheoryOfChangeItem;
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

export class Activity {
  id: number;
  name: string;
  project_id: number;
  prj_id: number;
  intervention_id: number;
  parent_id: number;
  editing_user_id: number;
  toc_indicator_id: number;
  owner_id: number;
  status_id: number;
  notes: string = "";
  url: string = "";

  driver_ids: number[] = [];
}

export class Schedule {
  id: number = 0;
  editing_user_id: number = 0;
  activity_id: number = 0;
  planned_date_from: Date = new Date(2007, 9, 26);
  planned_date_to: Date = new Date(2022, 9, 26);
  actual_date_from: Date = new Date(2007, 9, 26);
  actual_date_to: Date = new Date(2022, 9, 26);
  dependency_ids: number[] = [];
  owner_id: number = 0;
  participant_id: number = 0;
  status_id: number = 0;
  notes: string = "";
  url: string = "";
}

export class Monitoring {
  id: number;
  target?: number;
  baseline?: number;
  data_collection_method?: string;
  data_collection_frequency?: string;
  evaluation: { [key: string]: number } = {};
  evaluation_period?: "monthly" | "weekly" | "quarterly";

  toc_item_indicator_id?: number;
  project_id?: number;

  toc_item_indicator: TheoryOfChangeIndicator;
}
