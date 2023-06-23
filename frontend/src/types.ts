import type { Dayjs } from "dayjs";

export class User {
  id: number;
  email: string;
  name: string;
  address_as?: string;
  token?: string;
  last_project_id?: number;
  organisation_id?: number;
}

export class Project {
  id: number;
  name: string;
  start_date: Dayjs;
  end_date: Dayjs;
  country_id?: number;
}

export class LuIndiKit {
  id: number;
  name: string;
  wording_english: string;
  wording_french: string;
  wording_portuguese: string;
  wording_czech: string;
  guidance: string;
  section: string;
  sector: string;
  sub_sector?: string;
  indicator_level: string[];

  // TODO: To be provided by Petr
  purpose: string;
}

export class ProjectIndicator {
  id: number;
  name: string;
  indi_kit_id: number;
  project_id: number;

  indi_kit?: LuIndiKit;
}

/*
 * @deprecated
 */
export class IndicatorType {
  id: number;
  name: string = "";
  parent_id?: number;
}

/*
 * @deprecated
 */
export class IndicatorGroup {
  id: number;
  name: string = "";
  group_id: number;
  // level: string;
  phrasing: string = "";
  purpose: string = "";
  link: string = "";
}

/**
 * @deprecated
 */
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

// class TheoryOfChangeIndicator {
//   id: number;
//   toc_item_id: number;
//   indicator_id: number;
//   indicator: IndicatorGroup;

//   toc_item: TheoryOfChangeItem;
// }

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
  id: number;
  name: string = "";
  assumptions: string = "";
  description: string = "";
  type_id: number = undefined;
  from_id?: number = undefined;
  to_id?: number = undefined;
  sem_id?: number;
  project_id: number;
  is_validated: boolean = false;

  indicators: Array<TheoryOfChangeIndicator> = [];

  /**
   * @deprecated
   */
  graph: Array<TheoryOfChangeItem> = [];
  risks: Risk[] = [];
  // indicators: any[] = [];
}

export class TheoryOfChangeIndicator {
  id: number;
  indicator_id: number;
  theory_of_change_id: number;
  project_id: number;
  activity_id: number;

  indicator?: ProjectIndicator;

  project?: Project;
  theories_of_change?: TheoryOfChange;
}

export class Activity {
  id: number;
  name: string;
  project_id: number;
  prj_id: number;
  intervention_id: number;
  parent_id: number;
  editing_user_id: number;
  theory_of_change_id: number;
  owner_id: number;
  status_id: number;
  notes: string = "";
  url: string = "";
  driver_ids: number[] = [];

  // FIXME: REMOVE THIS
  /**
   * @deprecated
   */
  toc_indicator_id: number;
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

  toc_indicator: TheoryOfChangeIndicator;
}

export class ProjectData {
  id: number;
  q_id: number;
  prj_id: number;
  editing_user_id: number;
  theory_of_change_id: number;
  data: string;
  module?: "objectives" | "audiences";
  name?: "specific_objectives" | "secondary_audiences" | "primary_audiences";
}

export class Communication {
  id: number;
  project_id: number;
  title: string;
  message_objectives: string;
  delivery_platforms: string;
  format: string;
  key_points: string;
  contents: string;
  created_at: Date;
  updated_at: Date;
  deleted_at?: Date;

  indicators: Array<{
    id: number;
    communication_id: number;
    indicator_id: number;
  }> = [];

  project_objectives: Array<{
    id: number;
    communication_id: number;
    objective_id: number;
  }> = [];

  target_audiences: Array<{
    id: number;
    communication_id: number;
    audience_id: number;
  }> = [];

  drivers: Array<{
    id: number;
    communication_id: number;
    driver_id: number;
  }> = [];
}
