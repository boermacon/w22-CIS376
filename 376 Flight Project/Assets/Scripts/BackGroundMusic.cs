using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BackGroundMusic : MonoBehaviour
{
    private AudioSource bgMusic;
    // Start is called before the first frame update
    void Start()
    {
        bgMusic = gameObject.GetComponent<AudioSource>();

        if (SoundManager.mutedBG) {
            bgMusic.enabled = false;
        }
    }
}
