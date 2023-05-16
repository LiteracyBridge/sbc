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
    category: "ACCESS TO FOOD INDICATORS",
  },
];

export const INDICATORS = [
  {
    id: 1,
    groupId: 2,
    level: "process",
    name: "Sustainable Consumption and Production Indicators",
    summary:
      "% of [specify the target group] with a favourable attitude towards [specify the practice]",
    purpose:
      "People’s existing attitudes influence their willingness to adopt the practices promoted by development interventions. This indicator therefore measures the proportion of the target population with a favourable attitude towards following a given practice (this also includes usage of a certain product, such as solar lamps). The ‘target group’ can include many different stakeholders – farmers, businesses or the general public. ",
    notes: `1) Ask only about practices the respondents are likely to be familiar with, otherwise you will receive many unreliable or ‘I don’t know’ answers. If you talk about a product, consider showing the product or a photo of it (though do not provide any information about the product that might influence the respondent’s answer).

      2) The reliability of the data from this indicator depends on the practice you are asking about – the more people know what the ‘correct answer’ is, the less likely you are to receive reliable data (as people might be reluctant to say what they really think). Furthermore, keep in mind that the fact that someone has a positive attitude towards a certain behaviour does not automatically mean that s/he will adopt it (think of the health and other practices you approve of but do not necessarily follow). Remember: What matters the most are people’s actions, not knowledge or attitudes. Before you use this indicator, consider how likely it is that you will manage to get useful and reliable data.  `,
    dataCollection: `Determine the indicator’s value by using the following methodology:

    1) Define one or more statements that can be used to assess the respondents’ attitudes towards the promoted practice. For example: “Vegetable gardens should be watered in the early morning or late afternoon, not during middle of the day”. If you deal with a behaviour that is likely to be influenced by social desirability bias (respondents saying what the ‘correct’ answer is when it doesn’t correspond with what they really think), consider presenting the negative behaviour in the statement. For example: “When shopping, it is better to use plastic bags provided by the sellers instead of using reusable bags brought from home.” or “In order to have a good harvest of [specify the crop], a farmer must use chemical fertilizers. There is no other option.” In this case, the respondents who hold such unfavourable attitudes are more likely to admit to them.

    2) Conduct individual interviews with a representative sample of the target group members:

    RECOMMENDED SURVEY QUESTION (Q) AND POSSIBLE ANSWERS (A)

    Introduction: Now I am going to read a statement. Please show me on this scale the extent to which you agree or disagree with the statement [show the scale provided at the bottom of this page and explain how it works, including the meaning of each face]. There are no right or wrong answers – please answer according to your feelings about the statement.

    Q1: Which of these four faces [point to the scale] best represents your feelings about the following statement? [read the statement]

    A1: strongly agree / somewhat agree / somewhat disagree / strongly disagree / does not know

    3) Count the number of respondents who have a (‘somewhat’ or ‘strongly’) supportive attitude towards the eco-friendly practice.

    4) To calculate the indicator’s value, divide the number of respondents who have a supportive attitude by the total number of respondents (exclude those who did not know). Multiply the result by 100 to convert it to a percentage.
    `,
  },
  {
    id: 2,
    groupId: 4,
    level: "process",
    name: "Food Consumption Score",
    summary:
      "% of the target population with acceptable Food Consumption Score (FCS)",
    purpose:
      "The Food Consumption Score (FCS) is a more complex indicator of a household's food security status, as it considers not only dietary diversity and food frequency but also the relative nutritional importance of different food groups (on the other hand, its use of relatively long, 7 days recall period, might make the data less precise)",
    notes: `1) FCS is based on dietary diversity, not on Sphere recommendations of Kcal / day. In countries where the Food Basket is based on Kcal / day, it might not include enough proteins and dairy products. Therefore, achieving an “acceptable” FCS would be extremely difficult in spite of household members eating sufficient calorie intake.



    2) FCS is a good indicator of a household's food security; however, it does not help with understanding the quality of diets consumed by a specific group of household members, such as children 6-59 months of age.



    3) FCS is prone to seasonal variations. Do your best to collect baseline and endline data at the same time of the year; otherwise, it is very likely that they'll not be comparable (i.e. providing largely useless data).`,
    dataCollection: `Determine the indicator's value by using the following methodology:



    1) Conduct individual interviews with a representative sample of the target household representatives assessing how many days in the past 7 days the household has eaten any of the 16 pre-defined types of food by asking: "I would like to ask you about all the different foods that your household members have eaten in the last 7 days. During this period, how many days in the past 7 days has your household eaten ..." [name gradually all the 16 types of foods listed in WFP's FCS guidelines - access below].



    2) Sum up all the consumption frequencies of foods belonging to the same food groups (there is a total of 9 groups, as listed in WFP's FCS guidelines). Recode the frequency value of each food group above 7 as 7 (e.g. if the summed up frequency value is 10, recode it as 7).
    `,
  },
];
