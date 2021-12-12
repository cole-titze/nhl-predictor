library(readr)
library(mosaic)

hockey <- read_csv("C:\\Users\\colet\\DataspellProjects\\nhl-predictor\\Final.csv")

hockey <- as_tibble(hockey)
hockey <- subset(hockey, select=-c(Name, Wins, Losses, OTL, SHAPG, APG, SHAAPG ))


#tm1 <- lm(WP ~ GPG + GAPG + SOGPG + SOGAPG, data = hockey)

tm1 <- lm(WP ~ GPG + GAPG + SOGPG + SOGAPG, data = hockey)
summary(tm1)

# Example .73 wp
# 0.533653 + 0.200714(3.769231) - 0.204638*(2.807692) - 0.009540*(33.57692) + 0.008496*(31.38462) = 0.6619
# 0.533653 + 0.200714(3.769231) - 0.204638*(2.807692) - 0.009540*(33.57692) + 0.008496*(31.38462) = 0.6619