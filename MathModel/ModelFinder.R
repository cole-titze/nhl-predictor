library(readr)
library(leaps)
library(mosaic)

hockey <- read_csv("C:\\Users\\colet\\DataspellProjects\\nhl-predictor\\Final.csv")

hockey <- as_tibble(hockey)

hockey <- subset(hockey, select=-c(Name, Wins, Losses, OTL, SHAPG, APG, SHAAPG ))


base <- lm(WP~1, data=hockey)
full <- lm(WP~., data=hockey)
step(full,scope=list(upper=full,lower=base),direction="forward",trace=TRUE)

tm1 <- lm(WP ~ `Games Played` + GPG + PPG + `P/M` + PMPG +
  PPGPG + PPAPG + SHGPG + SOGPG + SOGP + GAPG + AAPG + PAPG +
  `Opp P/M` + PMAPG + PPGAPG + PPAAPG + SHGAPG + SOGAPG + SOGAP,
          data = hockey)
summary(tm1)

#tm1 <- lm(WP ~ `Games Played` + GPG + PPG + `P/M` + PMPG +
#            PPGPG + PPAPG + SHGPG + SOGPG + SOGP + GAPG + AAPG + PAPG +
#            `Opp P/M` + PMAPG + PPGAPG + PPAAPG + SHGAPG + SOGAPG + SOGAP,
#          data = hockey)

#tm1 <- lm(WP ~ GPG + PMPG +
#                        PPGPG + PPAPG + SHGPG + SOGPG + SOGP + GAPG  + PAPG +
#                        `Opp P/M` + SHGAPG + SOGAPG,
#                      data = hockey)