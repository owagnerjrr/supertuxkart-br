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
    struct RiderItemSlot
    {
        bool m_has_item;
        std::string m_item_ident;

        RiderItemSlot();
    };

    std::string m_front_rider_ident;
    std::string m_rear_rider_ident;
    bool m_front_is_active;
    RiderItemSlot m_front_item;
    RiderItemSlot m_rear_item;

    RiderItemSlot& getFrontItemSlot() { return m_front_item; }
    RiderItemSlot& getRearItemSlot() { return m_rear_item; }
    const RiderItemSlot& getFrontItemSlot() const { return m_front_item; }
    const RiderItemSlot& getRearItemSlot() const { return m_rear_item; }
    RiderItemSlot& getActiveItemSlot();
    RiderItemSlot& getReserveItemSlot();
    const RiderItemSlot& getActiveItemSlot() const;
    const RiderItemSlot& getReserveItemSlot() const;

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

    void setFrontRiderItem(const std::string& item_ident);
    void setRearRiderItem(const std::string& item_ident);
    void setActiveRiderItem(const std::string& item_ident);
    void setReserveRiderItem(const std::string& item_ident);
    void clearFrontRiderItem();
    void clearRearRiderItem();
    void clearActiveRiderItem();
    void clearReserveRiderItem();
    bool frontRiderHasItem() const { return m_front_item.m_has_item; }
    bool rearRiderHasItem() const { return m_rear_item.m_has_item; }
    bool activeRiderHasItem() const;
    bool reserveRiderHasItem() const;
    const std::string& getFrontRiderItemIdent() const;
    const std::string& getRearRiderItemIdent() const;
    const std::string& getActiveRiderItemIdent() const;
    const std::string& getReserveRiderItemIdent() const;
};

#endif

