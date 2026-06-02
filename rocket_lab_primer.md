# Rocket Lab: A Quick Primer

*Last updated: June 2026. Written for readers who are new to the company. Years and specs are verified against current sources; targets that have not yet happened are flagged as targets.*

If you arrived here wondering what "Rocket Lab," "Electron," and "Neutron" are, this page is your catch-up. It explains who the company is and why a data center launched on a Rocket Lab rocket is a serious idea rather than science fiction.

## Who Rocket Lab is

Rocket Lab was founded in **June 2006** by **Peter Beck**, a self-taught New Zealand engineer who became convinced there was a real market for cheap, frequent launches of small satellites. The company started in New Zealand, re-domiciled to the United States in 2013, and today is headquartered in **Long Beach, California**. It went public in **August 2021** and trades on the Nasdaq under the ticker **RKLB**.

The single most important thing to understand about Rocket Lab is that it is **vertically integrated**: it does not just launch rockets, it also designs and builds spacecraft and the components that go inside them. That full-stack reach matters a lot for the data-center idea this repo studies, and we will come back to it.

## Electron: the rocket that proved it could fly

Rocket Lab's first vehicle is **Electron**, a small-lift rocket. It reached orbit for the first time on **January 21, 2018** (a mission Beck cheekily named "Still Testing"), and it has been flying steadily ever since. Electron is a small launcher by design: it carries roughly **300 kg** to low Earth orbit, which is enough for a single small satellite or a cluster of tiny ones, not for anything heavy.

What makes Electron notable is not its size but its **track record**. By the end of 2025 it had flown roughly **80 missions**, and **2025 alone saw 21 launches with a 100% success rate**, a company record. That combination, flying often *and* landing the payload safely nearly every time, is hard to achieve and is exactly what customers pay for. Electron has made Rocket Lab one of the most active and reliable launch providers in the world after SpaceX.

Two engineering details are worth knowing. Electron is powered by **Rutherford engines**, which are largely **3D printed** and are the first **electric-pump-fed** engines to reach orbit (a battery-driven design that simplifies the plumbing of a traditional rocket engine). It flies from **Launch Complex 1 in Mahia, New Zealand**, and from **Launch Complex 2 at Wallops Island, Virginia**, giving the company launch sites in two hemispheres.

The takeaway: Electron established that Rocket Lab can build rockets, fly them often, and do it dependably.

## Not just launch: the spacecraft and components business

Here is the part many newcomers miss. Rocket Lab is **also a space hardware company**, and that side of the business is now its larger source of revenue. Through its Space Systems segment, Rocket Lab **sells the things that go to space, not just the ride**:

- **Satellite buses and platforms** (the body of a spacecraft that everything else bolts onto),
- and a long catalog of **subsystems**: solar panels, reaction wheels, star trackers, radios, separation systems, and more.

In plain terms, Rocket Lab can supply most of a working spacecraft from its own shelves and then launch it on its own rocket. For a project that imagines building and deploying many similar orbital nodes, that in-house breadth is a meaningful advantage: fewer outside vendors, more control over the whole stack.

## Neutron: the next, much bigger rocket

Rocket Lab's current headline project is **Neutron**, a **medium-lift, reusable** rocket that is being built now. Where Electron lifts a few hundred kilograms, Neutron is in a different weight class entirely. Its baseline target is about **13,000 kg to low Earth orbit while recovering and reusing the first stage** (roughly **15,000 kg** if the booster is expended and not reused). The first stage is designed to fly back and **land for reuse**, much like SpaceX's Falcon 9 booster. Neutron is powered by Rocket Lab's own new **Archimedes engines** (nine on the first stage, one on the upper stage) burning **liquid methane and liquid oxygen**.

Neutron's reuse strategy is worth understanding, because it is not just a smaller Falcon 9. Rocket Lab designed it around one idea: most of a rocket's cost, on the order of **85%, sits in the first stage** (the engines and the booster). So Neutron recovers and reuses that expensive first stage while keeping the second stage deliberately cheap and simple, essentially a light tank with a single engine. Falcon 9 reuses its booster too, but it throws away a more costly upper stage on every flight. And where SpaceX's Starship is chasing full, rapid reuse of both stages (a larger bet still being proven), Neutron takes the pragmatic route: reuse the part that is expensive, and make the part you expend cheap. If it works, that is an unusually efficient cost structure, arguably a smarter one than Falcon 9's.

The first flight is **targeted for late 2026** (the schedule has slipped more than once, so treat the date as a goal, not a guarantee).

Why does Neutron matter so much? Because **reusable medium-lift at low cost** has, until now, effectively meant one rocket from one company. Neutron aims to bring a **Falcon-9-class capability to a second provider**. A reusable booster is what turns launch from a rare, expensive event into something you can do frequently and affordably. That, in turn, is what makes ambitious plans realistic: lofting heavy payloads, and doing it again and again, on a schedule. Deploying a fleet of orbital data-center nodes is exactly the kind of mission that only becomes plausible once high-cadence, large-payload, low-cost launch exists.

## The arc, in one breath

Electron proved Rocket Lab can build and fly rockets reliably and at a high cadence. **Neutron scales that proven track record up to reusable medium-lift**, and reusable medium-lift is the enabler for the larger, repeatable missions, like an orbital data center, that the rest of this repo explores.

---

**Sources:** [Rocket Lab (official)](https://rocketlabcorp.com/launch/neutron/) · [Rocket Lab Electron (Wikipedia)](https://en.wikipedia.org/wiki/Rocket_Lab_Electron) · [Rocket Lab Neutron (Wikipedia)](https://en.wikipedia.org/wiki/Rocket_Lab_Neutron) · [SpaceNews: Rocket Lab wraps up record launch year](https://spacenews.com/rocket-lab-wraps-up-record-launch-year/) · [Spaceflight Now: Neutron debut slips to 2026](https://spaceflightnow.com/2025/11/11/rocket-lab-delays-debut-of-neutron-rocket-to-2026/)
