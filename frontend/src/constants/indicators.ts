// const indicatorTypes = [{ type: "sectoral", name: "Nutrition", id: 1 }];

export interface IIndicatorType {
  id: number;
  name?: string;
  parentId?: number;
  category?: string;
}

export const INDICATOR_TYPES: IIndicatorType[] = [
  {
    id: 1,
    name: "Nutrition",
  },
  {
    id: 2,
    parentId: 1,
    category: "Sustainable Consumption and Production Indicators",
  },
  {
    id: 3,
    name: "Food Security",
  },
  {
    id: 4,
    parentId: 3,
    category: "Access to Food Indicators",
  },
];

export const INDICATORS: Array<{
  id: number;
  name: string;
  groupId: number;
  // level: string;
  summary: string;
  purpose: string;
  link: string;
}> = [
  {
    id: 1,
    groupId: 2,
    // level: "process",
    name: "Ever Breastfed",
    summary:
      "% of [specify the target group] with a favourable attitude towards [specify the practice]",
    purpose:
      "People's existing attitudes influence their willingness to adopt the practices promoted by development interventions. This indicator therefore measures the proportion of the target population with a favourable attitude towards following a given practice (this also includes usage of a certain product, such as solar lamps). The 'target group' can include many different stakeholders - farmers, businesses or the general public. ",
    link: "https://www.indikit.net/indicator/1-nutrition/4432-ever-breastfed",
  },
  {
    id: 2,
    groupId: 4,
    // level: "process",
    name: "Food Consumption Score",
    summary:
      "% of the target population with acceptable Food Consumption Score (FCS)",
    purpose:
      "The Food Consumption Score (FCS) is a more complex indicator of a household's food security status, as it considers not only dietary diversity and food frequency but also the relative nutritional importance of different food groups (on the other hand, its use of relatively long, 7 days recall period, might make the data less precise)",
    link: "https://www.indikit.net/indicator/27-food-security/20-food-consumption-score",
  },
  {
    id: 2,
    groupId: 4,
    // level: "process",
    name: "Reduced Coping Strategy Index",
    summary: "average value of the Reduced Coping Strategies Index",
    purpose:
      "The Reduced Coping Strategies Index (RCSI) is a proxy indicator of household food insecurity. It considers both the frequency and severity of five pre-selected coping strategies that the household used in the seven days prior to the survey. It is a simplified version of the full Coping Strategies Index indicator",
    link: "https://www.indikit.net/indicator/27-food-security/3950-reduced-coping-strategy-index",
  },
];
