import type { Dayjs } from "dayjs";

export enum TheoryOfChangeType {
  Input = 1,
  Activity = 2,
  Output = 3,
  Outcome = 4,
  Impact = 5,
}

export const THEORY_OF_CHANGE_TYPES: Record<string, string> = {
  "1": "Input",
  "2": "Activity",
  "3": "Output",
  "4": "Outcome",
  "5": "Impact",
};

export enum ActivityStatus {
  Proposed = 1,
  Planned = 2,
  InProgress = 3,
  Completed = 4,
  Cancelled = 5,
}

export enum Importance {
  low = 1,
  medium = 2,
  high = 3,
}

export enum LibraryType {
  article = 1,
  "case_study" = 2,
  template = 3,
  evaluation = 4,
  date_collection_tool = 5,
}

// export enum AccessType {
//   Proposed = 1,
//   Planned = 2,
//   InProgress = 3,
//   Completed = 4,
//   Cancelled = 5,
// }

export const SEMS: Record<string, string> = {
  "1": "Individual",
  "2": "Interpersonal",
  "3": "Community",
  "4": "Organizational",
  "5": "Policy/Enabling environment",
};

export class GenericLookup {
  id: number;
  name: string;
  sequence?: number;
}

class Timestamps {
  deleted_by_id?: number;
  updated_at?: Date;
  created_at?: Date;
  deleted_at?: Date;
}

export class Organisation extends Timestamps {
  id: number;
  name: string;
  email?: string;
  website?: string;
  logo?: string;
  country_id: number;

  users: User[];
  projects: Project[];
}

export class User {
  id: number;
  email: string;
  sms?: string;
  whatsapp?: string;
  name: string;
  address_as?: string;
  token?: string;
  last_project_id?: number;
  organisation_id?: number;

  projects: ProjectUser[] = [];

  constructor(init?: Partial<User>) {
    Object.assign(this, init);

    this.projects ??= [];
  }
}

export class Stakeholder extends Timestamps {
  id: number;
  name?: string;
  description?: string;
  sms?: string;
  whatsapp?: string;
  email?: string;
  editing_user_id: number;
  project_id: number;
}

export class Project extends Timestamps {
  id: number;
  name: string;
  start_date: Dayjs;
  end_date: Dayjs;
  country_id?: number;
  archived: boolean = false;
  private_prj: boolean = true;
  evaluation_strategy?: string;
  feedback_strategy?: string;
  sustainability_strategy?: string;
  editing_user_id?: number;
  organisation_id?: number;

  organisation: Organisation;
  stakeholders: Stakeholder[] = [];
  users: ProjectUser[] = [];

  constructor(init?: Partial<Project>) {
    super();
    Object.assign(this, init);
  }
}

export class ProjectUser extends User {
  prj_id: number;
  access_id: number;
  user_id: number;

  project?: Project;
  user?: User;

  constructor(init?: Partial<ProjectUser>) {
    super(init);
    Object.assign(this, init);
  }
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

export class Intervention {
  id: number;
  name: string;
  url_description?: string;
  text_short?: string;
  text_long?: string;
  sequence?: number;
}

export class Driver {
  id: number;
  name: string;
  dgroup?: string;
  parent_id: number = 0;
  sequence?: number;
  sem_id?: number;
  text_short?: string;
  text_long?: string;
  url?: string;
  category_id?: number;
  framework_id?: number;
  intervention_ids?: number[];
}

export class ProjectDriver extends Driver {
  prj_id: number;
  editing_user_id?: number;
  lu_driver_id?: number;
  importance_id?: number;
  notes_context?: string;
  notes_gap?: string;
  notes_goal?: string;

  project?: Project;
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

export class TheoryOfChange {
  id: number;
  name: string = "";
  // assumptions: string = "";
  description: string = "";
  editing_user_id?: number;
  type_id: number = undefined;
  from_id?: number = undefined;
  to_id?: number = undefined;
  sem_id?: number;
  project_id: number;
  is_validated: boolean = false;
  links_to: number[] = [];

  indicators: Array<TheoryOfChangeIndicator> = [];

  /**
   * @deprecated
   */
  // graph: Array<TheoryOfChangeItem> = [];
  // risks: Risk[] = [];
  // indicators: any[] = [];
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

  toc_from?: TheoryOfChange;
  toc_to?: TheoryOfChange;
}

export class TheoryOfChangeIndicator {
  name: string;
  id: number;
  indikit_id: number;
  theory_of_change_id: number;
  project_id: number;
  activity_id: number;

  // indicator_id: number;
  // indicator?: ProjectIndicator;

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
  start_date?: Dayjs;
  end_date?: Dayjs;
  created_at?: Dayjs;
  updated_at?: Dayjs;
  deleted_at?: Dayjs;

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
  target?: string;
  baseline?: string;
  data_collection_method?: string;
  progress?: string | number;
  evaluation: Array<{ value: number; period: string }> = [];
  reporting_period?:
    | "Monthly"
    | "Weekly"
    | "Quarterly"
    | "Annually"
    | "Semi-Annually";
  toc_item_indicator_id?: number;
  project_id?: number;
  type: "Quantitative" | "Qualitative" | "Percentage";
  toc_indicator: TheoryOfChangeIndicator;
}

export enum ProjectDataName {
  specific_objective = "specific_objective",
  secondary_audience = "secondary_audience",
  primary_audience = "primary_audience",
  sector = "sector",
}

export enum ProjectDataModule {
  objectives = "objectives",
  audiences = "audiences",
  project_info = "project_info",
  basics = "basics",
  background = "background",
}

export class ProjectData {
  id: number;
  q_id: number;
  prj_id: number;
  editing_user_id: number;
  theory_of_change_id: number;
  data: string;
  module?: ProjectDataModule;
  name?: ProjectDataName;
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

export class MessageReceived extends Timestamps {
  id: number;
  message: string;
  channel: "w" | "s";
  user_id: number;
  message_sid: string;
  stakeholder_id: number;
  related_msg_id: number;

  user?: User;
  stakeholder?: Stakeholder;
  related_msg?: MessageSent;
}

export class MessageSent extends Timestamps {
  id: number;
  message: string;
  sent_time: Date;
  related_item: string;
  user_id_sending: number;
  prj_id: number;

  user?: User;
  project?: Project;
  replies: MessageReceived[] = [];
}
