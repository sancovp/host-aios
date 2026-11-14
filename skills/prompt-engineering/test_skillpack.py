"""D4 metaformal test: write_skill places skills COORDINATE-ADDRESSED via skilltree.
Trigger the substrate (skilltree.emit), OBSERVE the state change (skilltree.json + the emit report).
No API; needs the `agent-skilltree` dep (declared in pyproject)."""
import tempfile
from pathlib import Path

from prompt_engineering import write_skill, cohere_skills


def test_write_skill_plain_unchanged():
    """Default (coordinate=False) preserves the original behavior — no skilltree side-effect."""
    with tempfile.TemporaryDirectory() as t:
        p = write_skill("Plain One", "the plain skill", "# Plain\nbody", out_dir=t)
        assert p.name == "SKILL.md" and p.exists()
        assert (Path(t) / "plain-one" / "SKILL.md").exists()
        assert not (Path(t) / "skilltree.json").exists(), "default must not touch skilltree"
    print("ok  write_skill default behavior unchanged (no skilltree side-effect)")


def test_write_skill_coordinate():
    """D4 — coordinate=True places the skill as a coordinate-addressed node (skilltree.json written)."""
    with tempfile.TemporaryDirectory() as t:
        import skilltree
        write_skill("Alpha One", "the alpha skill", "# Alpha\nbody", out_dir=t, coordinate=True)
        write_skill("Beta Two", "the beta skill", "# Beta\nbody", out_dir=t, coordinate=True)
        report = cohere_skills(t)                       # cohere the finished forest ONCE
        assert report.get("ok"), report
        assert (Path(t) / "skilltree.json").exists(), "cohere must write skilltree.json"
        # OBSERVE the substrate: discover the tree back; each skill is a node with a hierarchical coord
        coords = {}
        def walk(n):
            coords[skilltree.skill_name(n)] = n.coord
            for c in n.children:
                walk(c)
        walk(skilltree.discover(t).root)
        placed = {nm: c for nm, c in coords.items() if "alpha-one" in nm or "beta-two" in nm}
        assert len(placed) == 2, f"both skills must be placed: {coords}"
        assert all(c and "." in c for c in placed.values()), f"skills must have child coordinates: {placed}"
    print("ok  D4: write_skill(coordinate=True) + cohere_skills -> coordinate-addressed", placed)


if __name__ == "__main__":
    test_write_skill_plain_unchanged()
    test_write_skill_coordinate()
    print("\nD4 SKILLPACK TESTS PASSED")
