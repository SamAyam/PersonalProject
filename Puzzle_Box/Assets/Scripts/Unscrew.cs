using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Unscrew : MonoBehaviour {
    public GameObject screw;
    public GameObject button;
    public GameObject sdvrIcon;
    public GameObject hiddenButton;
    public AudioSource speaker;
    public AudioClip turnSound;

    public void Turn()
    {
        if (sdvrIcon.activeInHierarchy)
        {
            screw.SetActive(false);
            button.SetActive(false);
            hiddenButton.SetActive(true);
            speaker.PlayOneShot(turnSound, 0.7F);
        }
    }
}
