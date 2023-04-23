using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
using UnityEngine.InputSystem;

//using Hashtable = ExitGames.Client.Photon.Hashtable;
using UnityEngine.Animations;



public class Enemy : MonoBehaviour
{
    #region Vars

    #region Location and Rotation Vars
    private float verticalLookRotation;
    bool grounded;
    Vector3 smoothMoveVelocity;
    Vector3 moveAmount;

    Vector3 moveDir, jumpDir;

    #endregion

    #region Player Vars
    Rigidbody rb;
    #endregion

    #region Health Vars
    private const float maxHealth = 45f;
    private float currentHealth = maxHealth;
    #endregion
    #endregion

    private float horizontalMovement;
    private float verticalMovement;
    private float distToGround = 0.2f;

    private float maxSpeed = 40;

    private Animator animator;

    private State currentState;
    private NavMeshAgent nav;
    private GameObject  player, guardObject;
    private bool guardable;

    public enum State
    {
        CHASING,
        GUARDING,
        SEARCHING
    }
    // Start is called before the first frame update
    void Start()
    {
        rb = gameObject.GetComponent<Rigidbody>();
        distToGround = gameObject.GetComponent<MeshCollider>().bounds.extents.y;
        animator = gameObject.GetComponent<Animator>();

        player = GameObject.Find("PlayerBear");
        nav = GetComponent<NavMeshAgent>();
        guardObject = GameObject.Find("Waypoint");

        currentState = State.GUARDING;
    }

    public IEnumerator Search()
    {
        currentState = State.SEARCHING;
        nav.isStopped = true;

        yield return new WaitForSeconds(2);
    }

    /// <summary>
    /// Update method called continously based on frame rate of user to handle local inputs
    /// </summary>
    private void Update()
    {
        if (guardObject != null)
        {
            guardable = true;
        }
        else
        {
            guardable = false;
        }
        float distance = Vector3.Distance(gameObject.transform.position, player.transform.position);

        if (distance < 50f)
        {
            currentState = State.CHASING;
        }
        if (distance > 50f && !guardable)
        {
            currentState = State.SEARCHING;
        }
        if (distance > 50f && guardable)
        {
            currentState = State.GUARDING;
        }



        if (nav.remainingDistance < 0.5f && currentState == State.SEARCHING)
        {
            if (!nav.pathPending)
            {
                nav.SetDestination(player.transform.position);
            }
        }

        if (currentState == State.CHASING)
        {
            nav.isStopped = false;
            if (!nav.pathPending)
            {
                nav.SetDestination(player.transform.position);
            }
        }

        if(currentState == State.GUARDING)
        {
            if (nav.remainingDistance < 1f)
            {
                nav.isStopped = true;
            }
            else
            {
                nav.SetDestination(guardObject.transform.position);
            }
        }

        //Make sure that the character only animates the idle animation while paused
        //Animation.SetFloat("InputX", 0);
        //Animation.SetFloat("InputZ", 0);

        //kill player controller if they fall into the void
        if (transform.position.y < -10f)
        {
            //Die();
        }
    }

    /// <summary>
    /// Method is called at a fixed rate instead of being tied to framerate like update() to move the character model around the game
    /// </summary>
    private void FixedUpdate()
    {
        
    }


    private void attack()
    {
    }

    public void damage(int damage)
    {
        currentHealth -= damage;
        guardable = true;
    }


    public void setGuardObject(GameObject guard)
    {
        guardObject = guard;
    }

    public Vector3 RandomNavmeshLocation(float radius)
    {
        Vector3 randomDirection = Random.insideUnitSphere * radius;
        randomDirection += transform.position;
        NavMeshHit hit;
        Vector3 finalPosition = Vector3.zero;
        if (NavMesh.SamplePosition(randomDirection, out hit, radius, 1))
        {
            finalPosition = hit.position;
        }
        return finalPosition;
    }
}