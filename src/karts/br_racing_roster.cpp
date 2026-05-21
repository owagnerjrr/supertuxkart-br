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
        Roster::SPECIES_CAT, "Gata rajada esperta e observadora.",
        "Boa aceleracao e controle fino nas curvas.", 1.00f, 1.12f, 1.15f, 1.04f });
    characters.push_back({ "vira_lata_preto", "Vira-lata Preto",
        Roster::SPECIES_DOG, "Cachorro preto brasileiro, agil e esperto.",
        "Arrancada boa e controle facil em curvas.", 1.00f, 1.08f, 1.08f, 1.00f });
    characters.push_back({ "gato_rajado", "Gato Rajado",
        Roster::SPECIES_CAT, "Gato rajado compacto, olhos atentos.",
        "Leve, tecnico e excelente para drift.", 0.96f, 1.12f, 1.16f, 0.98f });
    characters.push_back({ "capivara", "Capivara",
        Roster::SPECIES_CAPYBARA, "Capivara tranquila em kart robusto.",
        "Estavel e forte em disputas lado a lado.", 1.05f, 0.96f, 0.98f, 1.10f });
    characters.push_back({ "tucano", "Tucano",
        Roster::SPECIES_BIRD, "Tucano colorido com bico grande.",
        "Boa recuperacao e item forte.", 0.98f, 1.04f, 1.08f, 1.12f });
    characters.push_back({ "arara", "Arara",
        Roster::SPECIES_BIRD, "Arara azul e amarela, visual vibrante.",
        "Veloz em retas e boa em turbo.", 1.10f, 1.00f, 1.00f, 1.04f });
    characters.push_back({ "onca", "Onca",
        Roster::SPECIES_JAGUAR, "Onca-pintada forte e agressiva.",
        "Alta velocidade final e presenca pesada.", 1.16f, 0.92f, 0.94f, 1.08f });
    characters.push_back({ "lobo_guara", "Lobo-guara",
        Roster::SPECIES_MANED_WOLF, "Lobo-guara alto, laranja e elegante.",
        "Equilibrado, rapido e bom em retomada.", 1.08f, 1.04f, 1.02f, 1.00f });
    characters.push_back({ "tamandua", "Tamandua",
        Roster::SPECIES_ANTEATER, "Tamandua com cauda grande e postura calma.",
        "Peso medio, item bom e freada segura.", 1.02f, 0.98f, 1.02f, 1.14f });
    characters.push_back({ "quati", "Quati",
        Roster::SPECIES_COATI, "Quati curioso, rapido e pequeno.",
        "Aceleracao alta e curvas espertas.", 0.96f, 1.15f, 1.12f, 1.02f });
    characters.push_back({ "mico_leao", "Mico-leao",
        Roster::SPECIES_MONKEY, "Mico-leao-dourado expressivo.",
        "Leve, excelente para atalhos e turbo.", 0.98f, 1.10f, 1.12f, 1.08f });
    characters.push_back({ "jacare", "Jacare",
        Roster::SPECIES_CAIMAN, "Jacare baixo, resistente e sorrateiro.",
        "Kart pesado, forte no contato.", 1.07f, 0.90f, 0.92f, 1.16f });
    characters.push_back({ "preguica", "Preguica",
        Roster::SPECIES_SLOTH, "Preguica simpatica e relaxada.",
        "Baixa velocidade, mas muito facil de controlar.", 0.88f, 1.02f, 1.22f, 1.06f });
    characters.push_back({ "tatu_bola", "Tatu-bola",
        Roster::SPECIES_ARMADILLO, "Tatu-bola compacto com casco redondo.",
        "Defensivo, estavel e bom com itens.", 1.00f, 0.98f, 1.04f, 1.18f });

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
