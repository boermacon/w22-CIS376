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
    public const float maxHealth = 45f;
    public float currentHealth = maxHealth;
    private bool isDead = false;
    #endregion
    #endregion

    private float horizontalMovement;
    private float verticalMovement;
    private float distToGround = 0.2f;

    private float maxSpeed = 40;
    public float attackDamage = 1;

    private Animator animator;

    private State currentState;
    private NavMeshAgent nav;
    private GameObject  player, guardObject;
    private bool guardable;
    private bool attacking = false;

    public AudioClip audioClipHumanDeath;
    public AudioClip audioClipHumanAttack;
    private AudioSource audioSource;


    private const float chaseDistance = 50f;
    private const float attackDistance = 2.5f;

    public enum State
    {
        CHASING,
        GUARDING,
        SEARCHING,
        ATTACKING,
        DEAD
    }
    // Start is called before the first frame update
    void Start()
    {
        rb = gameObject.GetComponent<Rigidbody>();
        distToGround = gameObject.GetComponent<MeshCollider>().bounds.extents.y;
        animator = gameObject.GetComponent<Animator>();
        audioSource = GetComponent<AudioSource>();

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
        // Check to see if there is still and object to guard
        if (guardObject != null) { guardable = true; }
        else { guardable = false; }

        // Get the distance from this object to the player
        float distance = Vector3.Distance(gameObject.transform.position, player.transform.position);

        // Within distance chase
        if (distance < chaseDistance)
        {
            currentState = State.CHASING;
        }
        // If not within distance and there is no guardable object, serach for player
        if (distance > chaseDistance && !guardable)
        {
            currentState = State.SEARCHING;
        }
        // If not within distance and the is a guardable object, guard that object
        if (distance > chaseDistance && guardable)
        {
            currentState = State.GUARDING;
        }
        // If within attack distance, attack
        if (distance < attackDistance)
        {
            currentState = State.ATTACKING;
        }
        // If no health, die
        if (currentHealth <= 0)
        {
            currentState = State.DEAD;
        }

        // If chasing, navigate to player transform
        if (currentState == State.CHASING)
        {
            nav.isStopped = false;
            if (!nav.pathPending)
            {
                nav.SetDestination(player.transform.position);
            }
        }
        // If seraching and reached last search point, get new search point
        else if (currentState == State.SEARCHING && nav.remainingDistance < 0.5f)
        {
            if (!nav.pathPending)
            {
                nav.SetDestination(player.transform.position);
            }
        }
        // If guarding, branch
        if(currentState == State.GUARDING)
        {
            // Stop within 1f of guardable object
            if (nav.remainingDistance < 1f)
            {
                nav.isStopped = true;
            }
            // Move toward guardable object
            else
            {
                nav.SetDestination(guardObject.transform.position);
            }
        }
        // If attacking, attack
        else if (currentState == State.ATTACKING)
        {
            gameObject.transform.LookAt(player.transform);
            nav.isStopped = true;
            StartCoroutine(Attack());
        }
        // If dieing, die
        else if (currentState == State.DEAD)
        {
            if (!isDead)
            {
                Die();
            }
        }


        //Make sure that the character only animates the idle animation while paused
        //Animation.SetFloat("InputX", 0);
        //Animation.SetFloat("InputZ", 0);
        if (nav.speed > 0.1f || nav.speed < -0.1f)
        {
            animator.SetBool("WalkForward", true);
        }
        else
        {
            animator.SetBool("WalkForward", false);
        }

        //kill player controller if they fall into the void
        if (transform.position.y < -10f)
        {
            Destroy(gameObject);
        }
    }
    
    /// <summary>
    /// Method to destroy enemy on death.
    /// </summary>
    private void Die()
    {
        nav.isStopped = true;
        animator.Play("Death", 0, 0.0f);
        audioSource.clip = audioClipHumanDeath;
        audioSource.Play();
        Debug.Log("Enemy has died");
        rb.isKinematic = true;
        isDead = true;
    }

    /// <summary>
    /// Private coroutine to attack player.
    /// </summary>
    /// <returns></returns>
    private IEnumerator Attack() {
        // Check that we aren't currently attacking
        if (!attacking) {
            // Lock attack to true so no other attacks are flagged
            attacking = true;
            // Play attack animation and audio
            animator.Play("MeleeAttack_OneHanded", 0, 0.0f);
            audioSource.clip = audioClipHumanAttack;
            audioSource.Play();

            // Get playercontroller
            PlayerController playerStats = player.GetComponent<PlayerController>();
            
            // Damage player
            playerStats.Damage(attackDamage);
            
            //Wait a cooldown time
            yield return new WaitForSeconds(1.75f);
            
            // Open attack method to new attack instance.
            attacking = false;
        }
    }

    /// <summary>
    /// Public method to damage an enemey.
    /// </summary>
    /// <param name="damage">Float amount of damage to be removed from enemy health.</param>
    public void damage(float damage) { currentHealth -= damage; }

    /// <summary>
    /// Public setter to define the guardable object of an enemy.
    /// </summary>
    /// <param name="guard">GameObject that an enemy needs to guard.</param>
    public void setGuardObject(GameObject guard) { guardObject = guard; }

    /// <summary>
    /// Unused helper method
    /// </summary>
    /// <param name="radius"></param>
    /// <returns></returns>
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