using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyManager : MonoBehaviour
{
    private GameObject CokeHolder, WeedHolder, MethHolder;
    private GameObject CokeText, WeedText, MethText, DistanceText;
    private GameObject enemyPrefab;
    private int cokeAmt, weedAmt, methAmt;

    private int radius = 10;

    // Start is called before the first frame update
    void Start()
    {
        CokeHolder = GameObject.Find("CokeHolder");
        WeedHolder = GameObject.Find("WeedHolder");
        MethHolder = GameObject.Find("MethHolder");
        enemyPrefab = (GameObject)Resources.Load("HumanEnemy", typeof(GameObject));

        foreach (Transform tr in CokeHolder.transform)
        {
            Vector3 spawnPoint = tr.position;
            Vector3 randomDirection = Random.insideUnitSphere * radius;
            spawnPoint += randomDirection;
            spawnPoint.y = 1;
            Instantiate(enemyPrefab, spawnPoint, Quaternion.identity);
        }
        foreach (Transform tr in WeedHolder.transform)
        {
            Vector3 spawnPoint = tr.position;
            Vector3 randomDirection = Random.insideUnitSphere * radius;
            spawnPoint += randomDirection;
            spawnPoint.y = 1;
            Instantiate(enemyPrefab, spawnPoint, Quaternion.identity);
        }
        foreach (Transform tr in MethHolder.transform)
        {
            Vector3 spawnPoint = tr.position;
            Vector3 randomDirection = Random.insideUnitSphere * radius;
            spawnPoint += randomDirection;
            spawnPoint.y = 1;
            Instantiate(enemyPrefab, spawnPoint, Quaternion.identity);
        }
    }
}
