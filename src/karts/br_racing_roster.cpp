//
//  SuperTuxKart - a fun racing game with go-kart
//

#include "karts/br_racing_roster.hpp"

namespace
{
std::vector<BrazilianRacingRoster::Character> buildCharacterRoster()
{
    typedef BrazilianRacingRoster Roster;
    std::vector<Roster::Character> characters;

    characters.push_back({ "favela", "Favela",
        Roster::SPECIES_DOG, "Cachorra caramela alegre e brasileira.",
        "Equilibrada, carismatica e forte no turbo.", 1.08f, 1.06f, 1.06f, 1.08f });
    characters.push_back({ "atho", "Atho",
        Roster::SPECIES_CAT, "Gato preto com colar vermelho e cara brava.",
        "Leve, nervoso e excelente em drift curto.", 1.02f, 1.14f, 1.18f, 1.00f });
    characters.push_back({ "nina", "Nina",
        Roster::SPECIES_DOG, "Cachorra fila de grande porte.",
        "Pesada, rapida em reta e muito estavel.", 1.14f, 0.96f, 0.96f, 1.08f });
    characters.push_back({ "popo", "Popo",
        Roster::SPECIES_CAT, "Gata tricolor fofinha e esperta.",
        "Mais pesada, estavel e boa para segurar curvas.", 1.02f, 1.04f, 1.08f, 1.10f });

    return characters;
}

std::vector<BrazilianRacingRoster::SpeedClassInfo> buildSpeedClasses()
{
    typedef BrazilianRacingRoster Roster;
    std::vector<Roster::SpeedClassInfo> speed_classes;

    speed_classes.push_back({
        Roster::SPEED_CLASS_50_CC,
        "50cc",
        "50 cc",
        0.95f,
        1.08f,
        1.10f
    });

    speed_classes.push_back({
        Roster::SPEED_CLASS_100_CC,
        "100cc",
        "100 cc",
        1.15f,
        1.00f,
        1.00f
    });

    speed_classes.push_back({
        Roster::SPEED_CLASS_150_CC,
        "150cc",
        "150 cc",
        1.35f,
        0.94f,
        0.90f
    });

    return speed_classes;
}
}

// ----------------------------------------------------------------------------
const std::vector<BrazilianRacingRoster::Character>&
BrazilianRacingRoster::getCharacters()
{
    static const std::vector<Character> characters = buildCharacterRoster();
    return characters;
}

// ----------------------------------------------------------------------------
const std::vector<BrazilianRacingRoster::SpeedClassInfo>&
BrazilianRacingRoster::getSpeedClasses()
{
    static const std::vector<SpeedClassInfo> speed_classes = buildSpeedClasses();
    return speed_classes;
}

// ----------------------------------------------------------------------------
const BrazilianRacingRoster::Character*
BrazilianRacingRoster::getCharacter(const std::string& ident)
{
    const std::vector<Character>& characters = getCharacters();
    for (unsigned int i = 0; i < characters.size(); i++)
    {
        if (characters[i].m_ident == ident)
            return &characters[i];
    }
    return NULL;
}

// ----------------------------------------------------------------------------
const BrazilianRacingRoster::SpeedClassInfo*
BrazilianRacingRoster::getSpeedClass(SpeedClass speed_class)
{
    const std::vector<SpeedClassInfo>& speed_classes = getSpeedClasses();
    for (unsigned int i = 0; i < speed_classes.size(); i++)
    {
        if (speed_classes[i].m_class_id == speed_class)
            return &speed_classes[i];
    }
    return NULL;
}

// ----------------------------------------------------------------------------
const BrazilianRacingRoster::SpeedClassInfo*
BrazilianRacingRoster::getSpeedClass(const std::string& ident)
{
    const std::vector<SpeedClassInfo>& speed_classes = getSpeedClasses();
    for (unsigned int i = 0; i < speed_classes.size(); i++)
    {
        if (speed_classes[i].m_ident == ident)
            return &speed_classes[i];
    }
    return NULL;
}

// ----------------------------------------------------------------------------
std::string BrazilianRacingRoster::getDefaultPartnerIdent(
    const std::string& ident)
{
    if (ident == "atho")
        return "popo";
    if (ident == "popo")
        return "atho";
    if (ident == "favela")
        return "nina";
    if (ident == "nina")
        return "favela";

    const std::vector<Character>& characters = getCharacters();
    for (unsigned int i = 0; i < characters.size(); i++)
    {
        if (characters[i].m_ident == ident)
            return characters[(i + 1) % characters.size()].m_ident;
    }
    return std::string();
}

// ----------------------------------------------------------------------------
bool BrazilianRacingRoster::isValidTeamSelection(const TeamSelection& selection)
{
    return getCharacter(selection.m_front_rider_ident) != NULL &&
           getCharacter(selection.m_rear_rider_ident) != NULL &&
           selection.m_front_rider_ident != selection.m_rear_rider_ident &&
           getSpeedClass(selection.m_speed_class) != NULL;
}

// ----------------------------------------------------------------------------
std::string BrazilianRacingRoster::getTeamDisplayName(
    const TeamSelection& selection)
{
    const Character* front = getCharacter(selection.m_front_rider_ident);
    const Character* rear = getCharacter(selection.m_rear_rider_ident);

    if (front == NULL || rear == NULL)
        return std::string();

    return front->m_display_name + " + " + rear->m_display_name;
}
