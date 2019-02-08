using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class tear : MonoBehaviour {
    public GameObject thisButton;
    public GameObject closeBookButton;
    public GameObject key;
    public GameObject scissorsIcon;
    public GameObject pickUpKeyButton;
    public GameObject torn;
    public AudioClip cutSound;
    public AudioSource speaker;

	public void Cut()
    {
        if (scissorsIcon.activeInHierarchy)
        {
            thisButton.SetActive(false);
            closeBookButton.SetActive(false);
            key.SetActive(true);
            pickUpKeyButton.SetActive(true);
            torn.SetActive(true);
            speaker.PlayOneShot(cutSound, 0.7F);

        }
    }
}
