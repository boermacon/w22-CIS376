using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HealthManagerEnemy : MonoBehaviour
{
    public Image healthBar;
    public Enemy enemy;
    private float currentHealth;
    private float maxHealth;

    // Start is called before the first frame update
    void Start()
    {
        maxHealth = Enemy.maxHealth;
    }

    // Update is called once per frame
    void Update()
    {
        currentHealth = enemy.currentHealth;
        healthBar.fillAmount = enemy.currentHealth / Enemy.maxHealth;
    }
}
