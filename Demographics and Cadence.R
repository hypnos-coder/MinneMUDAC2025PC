library(readxl)
library(dplyr)
library(ggplot2)
#Novice <- read_excel("Downloads/Novice.xlsx")
library(readr)
library(car)
library(lubridate)

Novice <- read_csv("https://raw.githubusercontent.com/hypnos-coder/MinneMUDAC2025PC/refs/heads/hajar_dev/data/Imputed_Novice.csv")

Novice_filtered <- Novice %>%
  filter(`Match Length` >= 3)
summary(Novice_filtered)

Novice_filtered$`Big Gender` <- as.factor(Novice_filtered$`Big Gender`)

Novice_filtered$`Closure Reason` <- as.factor(Novice_filtered$`Closure Reason`)

model <- lm(`Match Length` ~ `Big Age`, data = Novice_filtered)
summary(model)

par(mfrow = c(2, 2))
plot(model)

model_log <- lm(log(`Match Length`) ~ `Big Age`, data = Novice_filtered)
summary(model_log)

par(mfrow = c(2, 2))
plot(model_log)


get_race <- function(race) {
  if (is.na(race)) return(NA_character_)
  races <- unlist(strsplit(race, ";"))
  first_race <- trimws(races[1])
  case_when(
    first_race == "Black or African American" ~ "Black or African American",
    first_race == "White or Caucasian" ~ "White or Caucasian",
    first_race == "Asian" ~ "Asian",
    first_race == "Pacific Islander" ~ "Pacific Islander",
    first_race == "Middle Eastern or North African" ~ "Middle Eastern or North African",
    first_race == "American Indian or Alaska Native" ~ "American Indian or Alaska Native",
    first_race == "Hispanic" ~ "Hispanic",
    first_race == "Other" ~ "Other",
    first_race == "Prefer not to say" ~ "Prefer not to say",
    TRUE ~ "Other/Unknown"
  )
}

Novice_filtered <- Novice_filtered %>%
  mutate(
    BigRaceCollapsed = sapply(`Big Race/Ethnicity`, get_race),
    LittleRaceCollapsed = sapply(`Little Participant: Race/Ethnicity`, get_race)
  ) %>%
  mutate(
    BigRaceCollapsed = as.factor(BigRaceCollapsed),
    LittleRaceCollapsed = as.factor(LittleRaceCollapsed)
  )

model_interact <- lm(`Match Length` ~ `Big Age` * `Big Gender` * BigRaceCollapsed, data = Novice_filtered)
summary(model_interact)

par(mfrow = c(2, 2))
plot(model_interact)

model_2way <- lm(`Match Length` ~ `Big Age` * `Big Gender` + BigRaceCollapsed, data = Novice_filtered)
summary(model_2way)

par(mfrow = c(2, 2))
plot(model_2way)

ggplot(Novice_filtered, aes(x = `Big Age`, y = `Match Length`, color = `Big Gender`)) +
  geom_point(alpha = 0.3) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 1.2) +
  labs(
    title = "Interaction of Big Age and Gender on Match Length",
    x = "Big Age (Years)",
    y = "Match Length (Months)"
  ) +
  theme_minimal()


#LITTLES AGES; RACE; GENDER

Novice_filtered <- Novice_filtered %>%
  mutate(
    LittleAge = interval(start = `Little Birthdate`, end = `Match Activation Date`) / years(1)
  )

ggplot(Novice_filtered, aes(x = LittleAge)) +
  geom_histogram(bins = 30, fill = "green", color = "black") +
  labs(
    title = "Distribution of Littles' Age at Match Activation",
    x = "Age (Years)",
    y = "Frequency"
  ) +
  theme_minimal()

model_little_age <- lm(`Match Length` ~ LittleAge, data = Novice_filtered)
summary(model_little_age)

par(mfrow = c(2, 2))
plot(model_little_age)


##ADDITIVE MODEL
model_additive <- lm(log(`Match Length`) ~ 
                       `Big Age` + `Big Gender` + BigRaceCollapsed + 
                       LittleAge + `Little Gender` + LittleRaceCollapsed, 
                     data = Novice_filtered)
summary(model_additive)

par(mfrow = c(2, 2))
plot(model_additive)
vif(model_additive)

Novice_filtered <- Novice %>%
  filter(`Match Length` >= 3)

#little age at match activation
Novice_filtered <- Novice_filtered %>%
  mutate(
    `Match Activation Date` = as.Date(`Match Activation Date`),
    `Little Birthdate` = as.Date(`Little Birthdate`),
    LittleAge = interval(`Little Birthdate`, `Match Activation Date`) / years(1)
  )

# mean Match Length by age group and Closure Reason
Novice_filtered %>%
  mutate(AgeGroup = cut(LittleAge, breaks = c(5, 10, 13, 16, 18), right = FALSE)) %>%
  group_by(AgeGroup, `Closure Reason`) %>%
  summarise(AvgMatchLength = mean(`Match Length`, na.rm = TRUE), n = n()) %>%
  arrange(desc(n))

#little age was significant and decreased match length so this portion is checking 
#if thats true
closure_table <- Novice_filtered %>%
  mutate(
    AgeGroup = cut(LittleAge, breaks = c(5, 10, 13, 16, 18), right = FALSE),
    ClosureStatus = case_when(
      `Closure Reason` == "Successful match closure" ~ "Successful",
      `Closure Reason` == "Child: Graduated"~ "Successful",
      
      TRUE ~ "Unsuccessful"
    )
  ) %>%
  group_by(AgeGroup, ClosureStatus) %>%
  summarise(n = n(), .groups = "drop") %>%
  tidyr::pivot_wider(names_from = ClosureStatus, values_from = n, values_fill = 0)
print(closure_table)

##PAIRWISE 
emmeans(model_additive, pairwise ~ `Big Gender`)

emmeans(model_additive, pairwise ~ BigRaceCollapsed)

emmeans(model_additive, pairwise ~ `Little Gender`)

emmeans(model_additive, pairwise ~ LittleRaceCollapsed)



#Checking Alignment effecst on Match Length:

Novice_filtered <- Novice_filtered %>%
  mutate(
    Gender_Match = `Big Gender` == `Little Gender`,
    Race_Match = as.character(BigRaceCollapsed) == as.character(LittleRaceCollapsed),
    Age_Diff = abs(`Big Age` - LittleAge)
  )
model_alignment <- lm(log(`Match Length`) ~ 
                        Gender_Match + Race_Match + Age_Diff, 
                      data = Novice_filtered)
summary(model_alignment)
par(mfrow = c(2, 2))
plot(model_alignment)

interaction_model <- lm(log(`Match Length`) ~ Gender_Match * Race_Match, data = Novice_filtered)
summary(interaction_model)
par(mfrow = c(2, 2))
plot(interaction_model)


##CLOSURE REASON DISTRIBUTIONS BY DEMOGRAPHICS###

#Part 1 successful matches vs unsuccessful matches
Novice_filtered <- Novice_filtered %>%
  mutate(
    ClosureType = case_when(
      `Closure Reason` %in% c("Successful match closure", "Child: Graduated") ~ "Successful",
      TRUE ~ "Unsuccessful"
    ) %>% factor()
  )

model_closure <- glm(ClosureType ~ 
                       `Big Age` + `Big Gender` + BigRaceCollapsed +
                       LittleAge + `Little Gender` + LittleRaceCollapsed,
                     data = Novice_filtered, 
                     family = binomial)
summary(model_closure)
par(mfrow = c(2, 2))
plot(model_closure)

Novice_filtered <- Novice_filtered %>%
  mutate(AgeGroup = cut(LittleAge, breaks = c(5, 10, 13, 16, 18), right = FALSE))

model_agegroup <- glm(ClosureType ~ AgeGroup, data = Novice_filtered, family = binomial)
summary(model_agegroup)
model_interact <- glm(ClosureType ~ LittleAge * `Little Gender`, data = Novice_filtered, family = binomial)
summary(model_interact)

model_little_gender <- glm(ClosureType ~ `Little Gender`, 
                           data = Novice_filtered, 
                           family = binomial)

summary(model_little_gender)

model_little_race <- glm(ClosureType ~ LittleRaceCollapsed, 
                         data = Novice_filtered, 
                         family = binomial)

summary(model_little_race)

model_closure_alignment <- glm(ClosureType ~ Gender_Match + Race_Match + Age_Diff,
                               data = Novice_filtered, family = binomial)
summary(model_closure_alignment)

interaction_closure_model <- glm(ClosureType ~ Gender_Match * Race_Match,
                                 data = Novice_filtered, family = binomial)
summary(interaction_closure_model)


#Part2 specific closure reason distributions
Novice$`Closure Reason Cleaned` <- Novice$`Closure Reason`

# Recode Closure Reasons with simplifications
Novice$`Closure Reason Cleaned`[Novice$`Closure Reason` %in% c(
  "Child/Family: Moved",
  "Child/Family: Moved out of service area",
  "Child/Family: Moved within service area"
)] <- "Child/Family: Moved"

Novice$`Closure Reason Cleaned`[Novice$`Closure Reason` %in% c(
  "Child/Family: Lost contact with agency",
  "Child/Family: Lost contact with volunteer",
  "Child/Family: Lost contact with volunteer/agency"
)] <- "Child/Family: Lost contact with volunteer/agency"

Novice$`Closure Reason Cleaned`[Novice$`Closure Reason` %in% c(
  "Volunteer: Lost contact with agency",
  "Volunteer: Lost contact with child/agency",
  "Volunteer: Lost contact with child/family"
)] <- "Volunteer: Lost contact with child/agency"

Novice$`Closure Reason Cleaned`[Novice$`Closure Reason` %in% c(
  "Volunteer: Moved",
  "Volunteer: Moved out of service area",
  "Volunteer: Moved within service area"
)] <- "Volunteer: Moved"

Novice <- Novice %>%
  mutate(
    BigRaceCollapsed = sapply(`Big Race/Ethnicity`, get_race),
    LittleRaceCollapsed = sapply(`Little Participant: Race/Ethnicity`, get_race),
    BigRaceCollapsed = as.factor(BigRaceCollapsed),
    LittleRaceCollapsed = as.factor(LittleRaceCollapsed)
  )

###Success Predictors

Novice_filtered$MatchLength <- as.numeric(Novice_filtered$`Match Length`)
hist(Novice_filtered$MatchLength,
     main = "Match Length Distribution",
     xlab = "Match Length (Months)",
     col = "green",
     border = "black")
summary(Novice_filtered$MatchLength)
Novice_filtered <- Novice_filtered %>%
  mutate(SuccessComposite = case_when(
   `Closure Reason` %in% c("Child: Graduated", "Successful match closure") ~ "Successful",
    `Stage` == "Active" ~ "Successful",
    `Match Length` > 10 ~ "LikelySuccessful",  # Customize threshold (e.g., 1 year)
    TRUE ~ "Unsuccessful"
  ))%>%
  mutate(SuccessComposite = factor(SuccessComposite))

model_success <- glm(SuccessComposite ~ 
                       `Big Age` + `Big Gender` + BigRaceCollapsed +
                       LittleAge + `Little Gender` + LittleRaceCollapsed,
                     data = Novice_filtered, 
                     family = binomial)
summary(model_success)

library(mediation)
Novice_filtered$SuccessBinary <- as.numeric(Novice_filtered$SuccessComposite == "Successful")

model_m <- lm(`Match Length` ~ `Big Age`, data = Novice_filtered)
model_y <- glm(SuccessBinary ~ `Match Length` + `Big Age`, data = Novice_filtered, family = binomial)
med_result <- mediate(model.m = model_m, model.y = model_y, treat = "Big Age", mediator = "Match Length", boot = TRUE)
summary(med_result)

Novice_filtered <- Novice_filtered %>%
  mutate(Age_Diff = `Big Age` - LittleAge)
model_m <- lm(`Match Length` ~ Age_Diff, data = Novice_filtered)
model_y <- glm(SuccessBinary ~ `Match Length` + Age_Diff, data = Novice_filtered, family = binomial)
med_result2 <- mediate(model.m = model_m, model.y = model_y, treat = "Age_Diff", mediator = "Match Length", boot = TRUE)
summary(med_result2)

model_log <- lm(log(`Match Length`) ~ Gender_Match, data = Novice_filtered)
summary(model_log)

model_race_match <- lm(log(`Match Length`) ~ Race_Match, data = Novice_filtered)
summary(model_race_match)




#CADENCE DISTRIBUTION

Testing <- read_csv("https://raw.githubusercontent.com/hypnos-coder/MinneMUDAC2025PC/refs/heads/hajar_dev/data/Imputed_Training.csv")

Testing$`Completion Date` <- as.Date(Testing$`Completion Date`)

Testing <- Testing %>%
  arrange(`Match ID 18Char`, `Completion Date`) %>%
  group_by(`Match ID 18Char`) %>%
  mutate(Days_Between_Calls = as.numeric(difftime(`Completion Date`, lag(`Completion Date`), units = "days")))

cadence_data <- Testing %>%
  group_by(`Match ID 18Char`) %>%
  summarise(
    Avg_Cadence = mean(Days_Between_Calls, na.rm = TRUE),
    Match_Length = first(`Match Length`)
  )

model_cadence <- lm(Match_Length ~ Avg_Cadence, data = cadence_data)
summary(model_cadence)
par(mfrow = c(2, 2))
plot(model_cadence)
 
library(MASS)
cadence_data_clean <- cadence_data %>%
  filter(Match_Length > 0)

boxcox(lm(Match_Length ~ Avg_Cadence, data = cadence_data_clean), 
       lambda = seq(-2, 2, 0.1))

cadence_data_clean$Log_Match_Length <- log(cadence_data_clean$Match_Length)
model_log_cadence <- lm(Log_Match_Length ~ Avg_Cadence, data = cadence_data_clean)
summary(model_log_cadence)
par(mfrow = c(2, 2))
plot(model_log_cadence)

ggplot(cadence_data_clean, aes(x = Match_Length, y = Avg_Cadence)) +
  geom_point(alpha = 0.3, color="lightblue") +
  #geom_smooth(method = "lm", formula = y ~ exp(x), se = TRUE, color = "green", linewidth = 1.2) +
  labs(
    title = "Support Call Cadence vs Match Length in Months",
    x = "Match Length",
    y = "Average Days Between Support Calls"
  ) +
  theme_classic()


library(ggplot2)

ggplot(Novice_filtered, aes(x = LittleAge, y = `Match Length`)) +
  geom_point(alpha = 0.3, color = "lightblue") +
  geom_smooth(method = "lm", se = TRUE, color = "darkblue", linewidth = 1.2) +
  labs(
    title = "Effect of Littles' Age on Match Length",
    x = "Little Age at Match Activation Years",
    y = "Match Length in Months"
  ) +
  theme_classic()

ggplot(Novice_filtered, aes(x = LittleAge, fill = ClosureType)) +
  geom_histogram(position = "fill", bins = 30, color = "darkblue") +
  scale_y_continuous(labels = scales::percent) +
  scale_fill_manual(values = c("Successful" = "lightblue", "Unsuccessful" = "lightgray")) +
  labs(
    title = "Proportion of Successful Closures by Little's Age",
    x = "Little Age at Match Activation",
    y = "Proportion of Matches",
    fill = "Closure Type"
  ) +
  theme_classic()

library(ggplot2)


ggplot(Novice_filtered, aes(x = as.factor(Gender_Match), y = `Match Length`, fill = as.factor(Gender_Match))) +
  geom_boxplot(alpha = 0.6, outlier.shape = NA) +
  stat_summary(fun = mean, geom = "point", shape = 20, size = 4, color = "darkblue", fill = "blue") +
  scale_fill_manual(values = c("FALSE" = "lightgray", "TRUE" = "lightblue")) +
  scale_x_discrete(labels = c("No Gender Match", "Gender Match")) +
  labs(
    title = "Match Length by Gender Match Status",
    x = "Gender Match",
    y = "Match Length (Months)",
    fill = "Gender Match"
  ) +
  theme_classic()

ggplot(Novice_filtered, aes(x = `Age_Diff` , y =`Match Length`)) +
  geom_point(alpha = 0.3, color = "lightblue") +
  geom_smooth(method = "lm", se = TRUE, color = "darkblue", linewidth = 1.2) +
  labs(
    title = "Effect of Age Difference on Match Length",
    x = "Age Difference",
    y = "Match Length (Months)"
  ) +
  theme_classic()