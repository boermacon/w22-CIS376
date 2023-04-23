using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BearAttackZone : MonoBehaviour
{
    public PlayerController bear;
    public Collider attackZoneCollider;

    void OnTriggerStay (Collider other)
    {
        if (other.CompareTag("Enemy"))
        {
            DealDamage(other);
        }
    }

    void DealDamage(Collider enemy)
    {
        Enemy enemyStats = enemy.GetComponent<Enemy>();
        enemyStats.damage(bear.attackDamage);
        // Debug.Log("Enemy Hit");
        // Debug.Log("Enemy HP: " + enemyStats.currentHealth);
    }
}
