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

    characters.push_back({
        "atho",
        "Atho",
        Roster::SPECIES_CAT,
        "Gato preto pequeno, olhos amarelos e colar vermelho.",
        "Especialista em curvas fechadas e arrancadas curtas.",
        0.94f,
        1.08f,
        1.15f,
        0.96f
    });

    characters.push_back({
        "popo",
        "Popo",
        Roster::SPECIES_CAT,
        "Gata rajada de tres cores, pelagem branca, preta e caramelo.",
        "Pilota equilibrada, boa para aprender pistas novas.",
        1.00f,
        1.00f,
        1.05f,
        1.00f
    });

    characters.push_back({
        "favela",
        "Favela",
        Roster::SPECIES_DOG,
        "Cachorra caramela, peito branco e postura alegre.",
        "Mascote veloz, forte em velocidade final.",
        1.10f,
        0.96f,
        0.94f,
        1.02f
    });

    characters.push_back({
        "nina",
        "Nina",
        Roster::SPECIES_DOG,
        "Cachorra maior, pelagem escura com marcas claras e colar.",
        "Personagem forte, estavel e boa para empurrar no pelotao.",
        1.05f,
        0.92f,
        0.98f,
        1.08f
    });

    characters.push_back({
        "mathias",
        "Mathias",
        Roster::SPECIES_DOG,
        "Poodle mais escuro, pelagem cacheada e perfil compacto.",
        "Leve e tecnico, bom para drift e recuperacao.",
        0.98f,
        1.12f,
        1.10f,
        0.98f
    });

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
        0.82f,
        1.08f,
        1.10f
    });

    speed_classes.push_back({
        Roster::SPEED_CLASS_100_CC,
        "100cc",
        "100 cc",
        1.00f,
        1.00f,
        1.00f
    });

    speed_classes.push_back({
        Roster::SPEED_CLASS_150_CC,
        "150cc",
        "150 cc",
        1.18f,
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
