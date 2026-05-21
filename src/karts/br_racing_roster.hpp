//
//  SuperTuxKart - a fun racing game with go-kart
//
//  BrazilianRacingRoster is the project-local roster seed for the
//  Double Dash-style Brazilian build.
//

#ifndef HEADER_BR_RACING_ROSTER_HPP
#define HEADER_BR_RACING_ROSTER_HPP

#include <string>
#include <vector>

class BrazilianRacingRoster
{
public:
    enum SpeedClass
    {
        SPEED_CLASS_50_CC,
        SPEED_CLASS_100_CC,
        SPEED_CLASS_150_CC
    };

    enum Species
    {
        SPECIES_CAT,
        SPECIES_DOG,
        SPECIES_CAPYBARA,
        SPECIES_BIRD,
        SPECIES_JAGUAR,
        SPECIES_MANED_WOLF,
        SPECIES_ANTEATER,
        SPECIES_COATI,
        SPECIES_MONKEY,
        SPECIES_CAIMAN,
        SPECIES_SLOTH,
        SPECIES_ARMADILLO
    };

    struct Character
    {
        std::string m_ident;
        std::string m_display_name;
        Species m_species;
        std::string m_visual_brief;
        std::string m_menu_role;
        float m_speed_bias;
        float m_acceleration_bias;
        float m_handling_bias;
        float m_item_bias;
    };

    struct SpeedClassInfo
    {
        SpeedClass m_class_id;
        std::string m_ident;
        std::string m_display_name;
        float m_speed_multiplier;
        float m_acceleration_multiplier;
        float m_turning_multiplier;
    };

    struct TeamSelection
    {
        std::string m_front_rider_ident;
        std::string m_rear_rider_ident;
        SpeedClass m_speed_class;
    };

    static const std::vector<Character>& getCharacters();
    static const std::vector<SpeedClassInfo>& getSpeedClasses();
    static const Character* getCharacter(const std::string& ident);
    static const SpeedClassInfo* getSpeedClass(SpeedClass speed_class);
    static const SpeedClassInfo* getSpeedClass(const std::string& ident);
    static bool isValidTeamSelection(const TeamSelection& selection);
    static std::string getTeamDisplayName(const TeamSelection& selection);
};

#endif
