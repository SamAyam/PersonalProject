using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UnlockCenter : MonoBehaviour
{

    public GameObject keyIcon;
    public GameObject keyhole;
    public GameObject moveButton;
    //public GameObject top;
    public GameObject thisButton;
    public AudioClip turnSound;
    public AudioSource speaker;


    public void Turn()
    {
        if (keyIcon.activeInHierarchy)
        {
            keyhole.transform.Rotate(0, 0, 90);
            moveButton.SetActive(true);
            thisButton.SetActive(false);
            speaker.PlayOneShot(turnSound);
        }
    }
}
