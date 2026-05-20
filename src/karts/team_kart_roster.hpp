//
//  SuperTuxKart - a fun racing game with go-kart
//
//  TeamKartRoster stores the two-rider state for Double Dash-style karts.
//  It is intentionally gameplay-only: rendering code can decide how to mount
//  each rider model on the front/rear sockets of the kart mesh.
//

#ifndef HEADER_TEAM_KART_ROSTER_HPP
#define HEADER_TEAM_KART_ROSTER_HPP

#include <string>

class TeamKartRoster
{
private:
    std::string m_front_rider_ident;
    std::string m_rear_rider_ident;
    bool m_front_is_active;

public:
    TeamKartRoster();
    TeamKartRoster(const std::string& front_rider_ident,
                   const std::string& rear_rider_ident);

    void setRiders(const std::string& front_rider_ident,
                   const std::string& rear_rider_ident);
    void swapRiders();

    const std::string& getFrontRiderIdent() const { return m_front_rider_ident; }
    const std::string& getRearRiderIdent() const { return m_rear_rider_ident; }
    const std::string& getActiveRiderIdent() const;
    const std::string& getItemRiderIdent() const;
    bool isFrontRiderActive() const { return m_front_is_active; }
    bool hasTwoRiders() const;
};

#endif

